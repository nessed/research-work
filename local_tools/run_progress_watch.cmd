@echo off
setlocal

cd /d C:\Users\Ali\Desktop\datalab_ali

C:\nvm4w\nodejs\claude.cmd -p "Run /progress-watch now for this repository. Follow the skill exactly and write CURRENT_PROGRESS.md plus the timestamped sitrep." --permission-mode acceptEdits --allowedTools "Bash,Read,Write,Edit,Glob,Grep,LS" --output-format text --max-budget-usd 1

