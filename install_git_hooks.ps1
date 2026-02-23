<#
Install Git hooks to use .githooks directory in this repo.
Run this once from the repository root (PowerShell):

    ./install_git_hooks.ps1

It sets `core.hooksPath` to .githooks for this repo.
#>

try {
    git rev-parse --is-inside-work-tree > $null 2>&1
} catch {
    Write-Error "Not a git repository. Initialize git in this folder or run inside a repo." ; exit 1
}

Write-Host "Setting Git hooks path to .githooks for this repository..."
git config core.hooksPath .githooks
if ($LASTEXITCODE -eq 0) {
    Write-Host "Git hooks path set. Ensure .githooks/post-commit is executable (on Windows it's fine)." -ForegroundColor Green
} else {
    Write-Error "Failed to set git config core.hooksPath. You may need to run as admin or set manually." -ForegroundColor Red
}
