#!/usr/bin/env python3
"""run_step04.py - multi-engine Step 04 claims extraction runner.

Pipeline position:
    Step 03 sections.jsonl -> Step 04 jobs.jsonl -> [THIS RUNNER]
    -> _supporting/job_results.jsonl -> Step 06 finalize (claims.jsonl) -> ...

This runner powers Step 5 (extraction) only. It reads a pre-built jobs.jsonl,
calls one of three interchangeable engines (gemini | claude | codex) per job,
accumulates results in _supporting/job_results.jsonl, tracks progress in
_supporting/run_state.json, and records terminal failures in
_supporting/failed_jobs/. It NEVER writes claims.jsonl -- that is Step 06.

Engines (all emit the same claim schema):
  gemini  Google Gemini Flash, free tier, google-genai SDK. Default bulk lane.
  claude  Claude Code subscription, headless (non-bare -> OAuth). Second lane.
  codex   OpenAI Codex CLI. Scalpel / reserve, used via --only-failed passes.

See the Step 04 stage runbook for the governance contract this honors.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import shutil
import sys
import tempfile
import time
import datetime as dt
from pathlib import Path

# jsonschema is optional. If present we do light per-claim validation; if not,
# the pipeline's Step 07 validator still runs downstream.
try:
    import jsonschema  # type: ignore
except Exception:  # pragma: no cover - environment dependent
    jsonschema = None

MAX_ATTEMPTS = 4
BACKOFFS = [2, 4, 8]  # seconds before attempts 2, 3, 4
DEFAULT_CHUNK = {"gemini": 8, "claude": 3, "codex": 1}


# --------------------------------------------------------------------------- #
# IO helpers
# --------------------------------------------------------------------------- #
def read_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    return records


def append_jsonl(path: Path, payload: object) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


# --------------------------------------------------------------------------- #
# Job / section handling
# --------------------------------------------------------------------------- #
def get_section_records(job: dict, job_id: str) -> list[dict]:
    for key in ("sections", "section_records", "records"):
        value = job.get(key)
        if isinstance(value, list):
            return value
    raise ValueError(
        f"job {job_id}: no section records found under 'sections', "
        f"'section_records', or 'records'"
    )


def chunk_list(items: list, size: int) -> list[list]:
    size = max(1, size)
    return [items[i : i + size] for i in range(0, len(items), size)]


def summarize_job_context(job: dict) -> str:
    """Human-readable content context for a failed job so it can be diagnosed
    without re-deriving anything: source file, section ids, page range, headings,
    numeric/table sensitivity, and a short text preview. Best-effort; never raises."""
    try:
        sections = get_section_records(job, str(job.get("job_id", "?")))
    except Exception:
        sections = []
    section_dicts = [s for s in sections if isinstance(s, dict)]
    source_file = job.get("source_file") or job.get("source_md_path") or "?"
    section_ids = [s.get("section_id") for s in section_dicts]
    starts = [s.get("start_page") for s in section_dicts if isinstance(s.get("start_page"), int)]
    ends = [s.get("end_page") for s in section_dicts if isinstance(s.get("end_page"), int)]
    page_range = f"{min(starts)}-{max(ends)}" if starts and ends else "?"
    headings: list = []
    for s in section_dicts:
        h = s.get("heading_text")
        if h and h not in headings:
            headings.append(h)
    numeric = any(bool(s.get("numeric_or_table_sensitive")) for s in section_dicts)
    preview = ""
    for s in section_dicts:
        if s.get("text"):
            preview = " ".join(str(s["text"]).split())[:200]
            break
    lines = [
        "--- content context (for diagnosis) ---",
        f"source_file: {source_file}",
        f"source_year: {job.get('source_year', '?')}",
        f"n_sections: {len(section_dicts)}",
        f"section_ids: {section_ids}",
        f"page_range: {page_range}",
        f"numeric_or_table_sensitive: {numeric}",
        f"headings ({len(headings)}): {headings[:10]}",
        f"text_preview: {preview}",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Prompt building
# --------------------------------------------------------------------------- #
def build_chunk_prompt(base_prompt: str, sections_chunk: list[dict]) -> str:
    payload = json.dumps(sections_chunk, ensure_ascii=False, indent=2)
    closing = (
        "Extract commentary claims ONLY from the section records above. Return a "
        "JSON array of claim records conforming to the frozen schema.\n\n"
        "Hard requirements for every claim:\n"
        "- `source_quote` MUST be a verbatim substring copied from the `text` of "
        "the exact section the claim is grounded in (do not paraphrase the quote).\n"
        "- `source_year` MUST be copied exactly from that section's metadata.\n"
        "- `source_page` MUST be copied from that section's page metadata "
        "(`start_page`, or another page inside `start_page`..`end_page`).\n"
        "- Do not invent fields, sections, or claims not supported by the section "
        "text above.\n\n"
        "Return JSON only: no prose, no Markdown code fences, no trailing commas."
    )
    return (
        base_prompt
        + "\n\n## Current Extraction Job Sections\n\n```json\n"
        + payload
        + "\n```\n\n"
        + closing
    )


# --------------------------------------------------------------------------- #
# Robust JSON parsing of model output
# --------------------------------------------------------------------------- #
def robust_json_parse(text: str) -> object:
    if text is None:
        raise ValueError("model returned no text")
    text = text.strip()
    if not text:
        raise ValueError("model returned empty output")

    # 1. direct
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2. fenced ```json ... ``` block
    fence = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if fence:
        try:
            return json.loads(fence.group(1))
        except json.JSONDecodeError:
            pass

    # 3. outermost array, then outermost object span
    for open_c, close_c in (("[", "]"), ("{", "}")):
        start = text.find(open_c)
        end = text.rfind(close_c)
        if 0 <= start < end:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                continue

    raise ValueError("could not parse JSON from model output")


def extract_claims(obj: object) -> list[dict]:
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for key in ("claims", "items", "data"):
            value = obj.get(key)
            if isinstance(value, list):
                return value
    raise ValueError("model output did not contain a claims array")


# --------------------------------------------------------------------------- #
# Per-claim validation (optional)
# --------------------------------------------------------------------------- #
def item_schema_of(schema: object) -> object:
    if isinstance(schema, dict) and schema.get("type") == "array" and "items" in schema:
        return schema["items"]
    return schema


def validate_claims(claims: list[dict], schema: object, job_id: str) -> None:
    if jsonschema is None:
        return
    validator_schema = item_schema_of(schema)
    for index, claim in enumerate(claims, 1):
        try:
            jsonschema.validate(claim, validator_schema)
        except jsonschema.ValidationError as exc:  # type: ignore[attr-defined]
            raise ValueError(
                f"{job_id} claim {index}: schema validation failed: {exc.message}"
            ) from exc


# --------------------------------------------------------------------------- #
# Rate limiting (--rpm pacing of request starts)
# --------------------------------------------------------------------------- #
class RateLimiter:
    def __init__(self, rpm: int | None) -> None:
        self.min_interval = 60.0 / rpm if rpm and rpm > 0 else 0.0
        self._lock = asyncio.Lock()
        self._next_start = 0.0

    async def wait(self) -> None:
        if self.min_interval <= 0:
            return
        async with self._lock:
            now = time.monotonic()
            delay = self._next_start - now
            if delay > 0:
                await asyncio.sleep(delay)
                now = time.monotonic()
            self._next_start = now + self.min_interval


# --------------------------------------------------------------------------- #
# Engine argv builders (shared by --dry-run and real execution)
# --------------------------------------------------------------------------- #
def build_claude_argv(claude_bin: str, schema_str: str, args: argparse.Namespace) -> list[str]:
    argv = [
        claude_bin,
        "-p",
        "--output-format",
        "json",
        "--json-schema",
        schema_str,
        "--mcp-config",
        '{"mcpServers":{}}',
        "--strict-mcp-config",
        "--max-turns",
        "1",
        "--no-session-persistence",
        "--permission-mode",
        "plan",
    ]
    if args.effort:
        argv += ["--effort", args.effort]
    if args.model:
        argv += ["--model", args.model]
    return argv


def build_codex_argv(
    codex_bin: str, schema_file: str, out_msg_file: str, args: argparse.Namespace
) -> list[str]:
    argv = [
        codex_bin,
        "exec",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--color",
        "never",
        "--output-schema",
        schema_file,
        "--output-last-message",
        out_msg_file,
        "-c",
        "model_reasoning_effort=low",
    ]
    if args.model:
        argv += ["-m", args.model]
    argv += ["-"]  # read prompt from stdin
    return argv


def codex_output_schema(schema: object) -> object:
    """Codex requires a top-level object schema. Wrap an array schema in
    {claims: [...]}; pass object schemas through unchanged."""
    if isinstance(schema, dict) and schema.get("type") == "array":
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Codex Step 04 wrapped claim extraction job output",
            "type": "object",
            "additionalProperties": False,
            "required": ["claims"],
            "properties": {"claims": schema},
        }
    return schema


# --------------------------------------------------------------------------- #
# Engine callers (each returns a list of raw claim dicts for one chunk)
# --------------------------------------------------------------------------- #
async def call_claude(
    prompt: str, schema: object, args: argparse.Namespace, claude_bin: str
) -> list[dict]:
    schema_str = json.dumps(schema, ensure_ascii=False)
    argv = build_claude_argv(claude_bin, schema_str, args)
    tmpdir = tempfile.mkdtemp(prefix="step04_claude_")
    try:
        proc = await asyncio.create_subprocess_exec(
            *argv,
            cwd=tmpdir,  # fresh empty dir: no CLAUDE.md / .mcp.json autoload
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, err = await proc.communicate(prompt.encode("utf-8"))
        if proc.returncode != 0:
            raise RuntimeError(
                f"claude exit {proc.returncode}: "
                f"{err.decode('utf-8', 'replace').strip()[:500]}"
            )
        wrapper = json.loads(out.decode("utf-8", "replace"))
        if wrapper.get("is_error"):
            raise RuntimeError(f"claude error result: {str(wrapper.get('result'))[:500]}")
        # Prefer the conforming object in structured_output; fall back to result text.
        if wrapper.get("structured_output") is not None:
            obj = wrapper["structured_output"]
        else:
            obj = robust_json_parse(wrapper.get("result"))
        return extract_claims(obj)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


async def call_codex(
    prompt: str, schema: object, args: argparse.Namespace, codex_bin: str
) -> list[dict]:
    tmpdir = tempfile.mkdtemp(prefix="step04_codex_")
    try:
        schema_file = Path(tmpdir) / "output_schema.json"
        out_msg_file = Path(tmpdir) / "last_message.txt"
        write_json(schema_file, codex_output_schema(schema))
        argv = build_codex_argv(codex_bin, str(schema_file), str(out_msg_file), args)
        proc = await asyncio.create_subprocess_exec(
            *argv,
            cwd=tmpdir,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, err = await proc.communicate(prompt.encode("utf-8"))
        if proc.returncode != 0:
            raise RuntimeError(
                f"codex exit {proc.returncode}: "
                f"{err.decode('utf-8', 'replace').strip()[:500]}"
            )
        raw = ""
        if out_msg_file.exists():
            raw = out_msg_file.read_text(encoding="utf-8", errors="replace").strip()
        if not raw:
            raw = out.decode("utf-8", "replace")
        return extract_claims(robust_json_parse(raw))
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def make_gemini_caller(args: argparse.Namespace, model: str):
    """Build an async gemini caller. Imports google-genai lazily and reads the
    API key from the environment. Exits clearly if either is unavailable."""
    try:
        from google import genai  # type: ignore
        from google.genai import types  # type: ignore
    except Exception as exc:  # pragma: no cover - environment dependent
        sys.exit(
            "engine 'gemini' requires the google-genai SDK. "
            "Install it with: pip install google-genai\n"
            f"(import error: {exc})"
        )

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        sys.exit("engine 'gemini' requires GEMINI_API_KEY (or GOOGLE_API_KEY) to be set.")

    client = genai.Client(api_key=api_key)
    # response_schema can choke on JSON-Schema features Gemini does not support
    # (additionalProperties:false, const, ...). Disable it for the rest of the
    # run the first time it is rejected; the prompt already carries the schema.
    use_schema = {"value": True}

    async def caller(prompt: str, schema: object) -> list[dict]:
        async def _generate(with_schema: bool):
            cfg_kwargs = {"response_mime_type": "application/json"}
            if with_schema:
                cfg_kwargs["response_schema"] = schema
            config = types.GenerateContentConfig(**cfg_kwargs)
            return await client.aio.models.generate_content(
                model=model, contents=prompt, config=config
            )

        if use_schema["value"]:
            try:
                resp = await _generate(True)
            except Exception as exc:
                # One immediate fallback without response_schema, then remember.
                use_schema["value"] = False
                print(
                    f"  note: gemini rejected response_schema, falling back to "
                    f"mime-only JSON for the rest of the run ({type(exc).__name__})",
                    file=sys.stderr,
                    flush=True,
                )
                resp = await _generate(False)
        else:
            resp = await _generate(False)

        return extract_claims(robust_json_parse(resp.text))

    return caller


# --------------------------------------------------------------------------- #
# Shared run state
# --------------------------------------------------------------------------- #
class RunState:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.last_engine: str | None = None
        self.completed: set[str] = set()
        self.failed: set[str] = set()
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                self.last_engine = data.get("last_engine")
                self.completed = set(data.get("completed", []) or [])
                self.failed = set(data.get("failed", []) or [])
            except Exception:
                pass  # corrupt/partial state -> start fresh, don't crash

    def write(self) -> None:
        write_json(
            self.path,
            {
                "last_engine": self.last_engine,
                "completed": sorted(self.completed),
                "failed": sorted(self.failed),
                "n_completed": len(self.completed),
                "n_failed": len(self.failed),
                "updated": now_iso(),
            },
        )


# --------------------------------------------------------------------------- #
# Per-job processing
# --------------------------------------------------------------------------- #
async def process_job(
    job: dict,
    *,
    base_prompt: str,
    schema: object,
    engine: str,
    chunk_size: int,
    engine_call,
    sem: asyncio.Semaphore,
    lock: asyncio.Lock,
    limiter: RateLimiter,
    state: RunState,
    job_results_path: Path,
    failed_jobs_dir: Path,
) -> None:
    job_id = job.get("job_id") or "<missing job_id>"

    async def record_failure(message: str) -> None:
        async with lock:
            (failed_jobs_dir / f"{job_id}.txt").write_text(
                f"engine: {engine}\njob_id: {job_id}\nts: {now_iso()}\n\n"
                f"{message}\n\n{summarize_job_context(job)}\n",
                encoding="utf-8",
            )
            state.failed.add(job_id)
            state.completed.discard(job_id)
            state.last_engine = engine
            state.write()
        print(f"FAIL {job_id}: {message.splitlines()[0]}", file=sys.stderr, flush=True)

    # Resolve section records up front; a malformed job fails loudly by name.
    try:
        sections = get_section_records(job, job_id)
    except Exception as exc:
        await record_failure(f"could not load section records: {exc}")
        return

    chunks = chunk_list(sections, chunk_size)
    last_err: str = ""

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            async with sem:
                claims: list[dict] = []
                for chunk in chunks:
                    prompt = build_chunk_prompt(base_prompt, chunk)
                    await limiter.wait()
                    claims.extend(await engine_call(prompt))
            validate_claims(claims, schema, job_id)

            async with lock:
                append_jsonl(
                    job_results_path,
                    {
                        "job_id": job_id,
                        "engine": engine,
                        "n_sections": len(sections),
                        "n_claims": len(claims),
                        "claims": claims,
                        "ts": now_iso(),
                    },
                )
                state.completed.add(job_id)
                state.failed.discard(job_id)
                state.last_engine = engine
                state.write()
            print(f"ok {job_id}: {len(claims)} claims via {engine}", flush=True)
            return
        except Exception as exc:
            last_err = f"{type(exc).__name__}: {exc}"
            if attempt < MAX_ATTEMPTS:
                await asyncio.sleep(BACKOFFS[attempt - 1])
            else:
                await record_failure(f"failed after {MAX_ATTEMPTS} attempts: {last_err}")


# --------------------------------------------------------------------------- #
# CLI / orchestration
# --------------------------------------------------------------------------- #
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Multi-engine Step 04 claims extraction runner "
        "(powers Step 5 extraction; never writes claims.jsonl).",
    )
    parser.add_argument("--engine", required=True, choices=["gemini", "claude", "codex"])
    parser.add_argument("--run-dir", required=True, help="Step 04 run folder")
    parser.add_argument("--schema-file", required=True, help="claim output JSON schema")
    parser.add_argument("--prompt-file", required=True, help="extraction prompt markdown")
    parser.add_argument("--jobs", default=None, help="default: <run-dir>/_supporting/jobs.jsonl")
    parser.add_argument("--concurrency", type=int, default=3)
    parser.add_argument("--chunk", type=int, default=None, help="sections per model call")
    parser.add_argument("--shard", type=int, default=0)
    parser.add_argument("--num-shards", type=int, default=1)
    parser.add_argument("--only-failed", action="store_true")
    parser.add_argument("--effort", choices=["low", "medium", "high", "max"], default=None)
    parser.add_argument("--model", default=None, help="per-engine model override")
    parser.add_argument("--rpm", type=int, default=None, help="request pacing per minute")
    parser.add_argument("--dry-run", action="store_true", help="print engine argv and exit")
    return parser.parse_args(argv)


def resolve_binary(*names: str) -> str | None:
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    return None


def select_jobs(
    jobs: list[dict], args: argparse.Namespace, state: RunState
) -> list[dict]:
    if args.only_failed:
        # Process exactly the jobs currently in failed[]; no sharding.
        return [j for j in jobs if (j.get("job_id") in state.failed)]

    if args.num_shards < 1 or not (0 <= args.shard < args.num_shards):
        sys.exit(
            f"invalid shard config: --shard {args.shard} --num-shards {args.num_shards}"
        )
    selected = []
    for index, job in enumerate(jobs):
        if index % args.num_shards != args.shard:
            continue
        if job.get("job_id") in state.completed:
            continue
        selected.append(job)
    return selected


def do_dry_run(args: argparse.Namespace, schema: object) -> int:
    print(f"# dry-run: engine={args.engine}")
    print("# (prompt is sent on stdin; argv shown below)\n")
    if args.engine == "claude":
        claude_bin = resolve_binary("claude.cmd", "claude") or "claude.cmd"
        argv = build_claude_argv(claude_bin, json.dumps(schema, ensure_ascii=False), args)
        print(json.dumps(argv, ensure_ascii=False, indent=2))
    elif args.engine == "codex":
        codex_bin = resolve_binary("codex.cmd", "codex") or "codex.cmd"
        argv = build_codex_argv(
            codex_bin,
            "<tmp>/output_schema.json",
            "<tmp>/last_message.txt",
            args,
        )
        print(json.dumps(argv, ensure_ascii=False, indent=2))
        print("\n# codex output schema (top-level object) it would receive:")
        print(json.dumps(codex_output_schema(schema), ensure_ascii=False, indent=2)[:1200])
    else:  # gemini
        print(json.dumps(
            {
                "sdk": "google-genai",
                "model": args.model or "gemini-2.5-flash",
                "config": {
                    "response_mime_type": "application/json",
                    "response_schema": "<loaded schema dict>",
                },
                "needs_env": "GEMINI_API_KEY or GOOGLE_API_KEY",
            },
            indent=2,
        ))
    return 0


async def run(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    supporting = run_dir / "_supporting"
    supporting.mkdir(parents=True, exist_ok=True)
    jobs_path = Path(args.jobs).resolve() if args.jobs else supporting / "jobs.jsonl"
    job_results_path = supporting / "job_results.jsonl"
    run_state_path = supporting / "run_state.json"
    failed_jobs_dir = supporting / "failed_jobs"
    failed_jobs_dir.mkdir(exist_ok=True)

    if not jobs_path.exists():
        sys.exit(f"jobs file not found: {jobs_path}")
    schema = json.loads(Path(args.schema_file).read_text(encoding="utf-8"))
    base_prompt = Path(args.prompt_file).read_text(encoding="utf-8")

    chunk_size = args.chunk if args.chunk else DEFAULT_CHUNK[args.engine]

    if args.dry_run:
        return do_dry_run(args, schema)

    if jsonschema is None:
        print(
            "note: jsonschema not importable; skipping per-claim validation "
            "(Step 07 validator still runs downstream).",
            flush=True,
        )

    jobs = read_jsonl(jobs_path)
    state = RunState(run_state_path)

    # Build the engine caller bound to its resources.
    if args.engine == "claude":
        claude_bin = resolve_binary("claude.cmd", "claude")
        if not claude_bin:
            sys.exit("could not find 'claude.cmd' or 'claude' on PATH")

        async def engine_call(prompt: str) -> list[dict]:
            return await call_claude(prompt, schema, args, claude_bin)

    elif args.engine == "codex":
        codex_bin = resolve_binary("codex.cmd", "codex")
        if not codex_bin:
            sys.exit("could not find 'codex.cmd' or 'codex' on PATH")

        async def engine_call(prompt: str) -> list[dict]:
            return await call_codex(prompt, schema, args, codex_bin)

    else:  # gemini
        gemini_caller = make_gemini_caller(args, args.model or "gemini-2.5-flash")

        async def engine_call(prompt: str) -> list[dict]:
            return await gemini_caller(prompt, schema)

    targets = select_jobs(jobs, args, state)
    mode = "only-failed" if args.only_failed else f"shard {args.shard}/{args.num_shards}"
    print(
        f"engine={args.engine} chunk={chunk_size} concurrency={args.concurrency} "
        f"{mode}: {len(targets)} job(s) to process "
        f"(of {len(jobs)} total; {len(state.completed)} already completed).",
        flush=True,
    )
    if not targets:
        print("nothing to do.", flush=True)
        return 0

    sem = asyncio.Semaphore(max(1, args.concurrency))
    lock = asyncio.Lock()
    limiter = RateLimiter(args.rpm)

    await asyncio.gather(
        *(
            process_job(
                job,
                base_prompt=base_prompt,
                schema=schema,
                engine=args.engine,
                chunk_size=chunk_size,
                engine_call=engine_call,
                sem=sem,
                lock=lock,
                limiter=limiter,
                state=state,
                job_results_path=job_results_path,
                failed_jobs_dir=failed_jobs_dir,
            )
            for job in targets
        )
    )

    state.write()
    print(
        f"done: {len(state.completed)} completed, {len(state.failed)} failed. "
        f"results -> {job_results_path}",
        flush=True,
    )
    return 1 if state.failed else 0


def main(argv: list[str] | None = None) -> int:
    if sys.platform == "win32":
        # Required for asyncio subprocesses on Windows. (It is also the default
        # loop on Windows since 3.8, but we set it explicitly per the runbook.
        # The policy API is deprecation-warned on 3.14+; silence that noise.)
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    args = parse_args(argv)
    return asyncio.run(run(args))


if __name__ == "__main__":
    raise SystemExit(main())
