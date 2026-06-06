# install_sitrep_skill.ps1
# Installs the /sitrep Claude Code skill into your project folder.
#
# Works no matter how you run it:
#   - from project root:        .\sitrep_skill_pack\install_sitrep_skill.ps1
#   - from inside the pack:      cd sitrep_skill_pack ; .\install_sitrep_skill.ps1
#
# In both cases the skill installs into the PROJECT ROOT (the folder that contains
# sitrep_skill_pack), not into the pack folder itself.
# Safe to re-run: it only creates folders and copies the skill file.

$ErrorActionPreference = "Stop"

# This script always lives at: <projectRoot>\sitrep_skill_pack\install_sitrep_skill.ps1
# So $PSScriptRoot is always the pack folder, and the project root is its parent —
# regardless of the current working directory the user ran it from.
$packRoot   = $PSScriptRoot
$projectDir = Split-Path -Parent $packRoot
$source     = Join-Path $packRoot "sitrep\SKILL.md"

Write-Host "Pack folder:    $packRoot"      -ForegroundColor DarkGray
Write-Host "Installing into: $projectDir"   -ForegroundColor Cyan

if (-not (Test-Path $source)) {
    throw "Cannot find skill source at '$source'. Keep install_sitrep_skill.ps1 next to the 'sitrep' folder inside sitrep_skill_pack."
}

# 1. Create .claude/skills/sitrep/
$skillDir = Join-Path $projectDir ".claude\skills\sitrep"
New-Item -ItemType Directory -Force -Path $skillDir | Out-Null
Write-Host "  created  $skillDir"

# 2. Copy sitrep/SKILL.md into .claude/skills/sitrep/SKILL.md
$dest = Join-Path $skillDir "SKILL.md"
Copy-Item -Path $source -Destination $dest -Force
Write-Host "  copied   SKILL.md -> $dest"

# 3. Create agentic/sitreps/
$sitrepsDir = Join-Path $projectDir "agentic\sitreps"
New-Item -ItemType Directory -Force -Path $sitrepsDir | Out-Null
Write-Host "  created  $sitrepsDir"

# 4. Create agentic/reviews/
$reviewsDir = Join-Path $projectDir "agentic\reviews"
New-Item -ItemType Directory -Force -Path $reviewsDir | Out-Null
Write-Host "  created  $reviewsDir"

Write-Host ""
Write-Host "Installed. Open Claude Code from the project root and run /sitrep." -ForegroundColor Green
Write-Host ""
