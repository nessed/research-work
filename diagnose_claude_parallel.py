import asyncio
import json
import time


CLAUDE_PS1 = r"C:\nvm4w\nodejs\claude.ps1"
JOBS = 7
CONCURRENCY = 3


async def run_job(job_id: int, sem: asyncio.Semaphore) -> dict:
    prompt = (
        "Return JSON only with this exact schema: "
        '{"job_id": number, "message": string}. '
        f"This is diagnostic job {job_id}."
    )

    async with sem:
        start = time.perf_counter()
        proc = await asyncio.create_subprocess_exec(
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            CLAUDE_PS1,
            "-p",
            prompt,
            "--max-turns",
            "1",
            "--output-format",
            "json",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        elapsed = time.perf_counter() - start

    stdout_text = stdout.decode("utf-8", errors="replace").strip()
    stderr_text = stderr.decode("utf-8", errors="replace").strip()
    result = None
    is_error = None
    try:
        parsed = json.loads(stdout_text)
        result = parsed.get("result")
        is_error = parsed.get("is_error")
    except json.JSONDecodeError:
        pass

    return {
        "job_id": job_id,
        "exit_code": proc.returncode,
        "elapsed_seconds": round(elapsed, 3),
        "is_error": is_error,
        "result_preview": result[:120] if isinstance(result, str) else None,
        "stdout_bytes": len(stdout),
        "stderr_bytes": len(stderr),
        "stderr_preview": stderr_text[:120] if stderr_text else None,
    }


async def main() -> None:
    sem = asyncio.Semaphore(CONCURRENCY)
    total_start = time.perf_counter()
    results = await asyncio.gather(*(run_job(i, sem) for i in range(1, JOBS + 1)))
    total_elapsed = time.perf_counter() - total_start

    print(json.dumps(
        {
            "jobs": JOBS,
            "concurrency": CONCURRENCY,
            "total_elapsed_seconds": round(total_elapsed, 3),
            "results": results,
        },
        indent=2,
    ))


if __name__ == "__main__":
    asyncio.run(main())
