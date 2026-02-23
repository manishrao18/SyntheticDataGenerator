<#
Backup helper for SyntheticDataGenerator

Usage examples:
- Run backup now:
    ./backup_code.ps1 -RunNow

- Register daily scheduled task that runs at 03:00 (requires admin):
    ./backup_code.ps1 -RegisterDaily -Time "03:00" -TaskName "SyntheticDataGeneratorBackup"

- Remove task:
    Unregister-ScheduledTask -TaskName "SyntheticDataGeneratorBackup" -Confirm:$false
#>

param(
    [switch]$RunNow,
    [switch]$RegisterDaily,
    [string]$Time = "03:00",
    [string]$TaskName = "SyntheticDataGeneratorBackup",
    [string]$PythonExe = "python"
)

$scriptPath = Join-Path $PSScriptRoot 'backup_code.py'

function Run-Backup {
    Write-Host "Running backup script: $scriptPath" -ForegroundColor Cyan
    try {
        & $PythonExe $scriptPath
        if ($LASTEXITCODE -ne 0) { Write-Warning "Backup script exited with code $LASTEXITCODE" }
    } catch {
        Write-Error "Failed to run backup script: $_"
    }
}

function Register-DailyTask {
    param(
        [string]$taskName,
        [string]$time
    )
    try {
        $action = New-ScheduledTaskAction -Execute $PythonExe -Argument ("`"`" + $scriptPath + "`"`")
        $trigger = New-ScheduledTaskTrigger -Daily -At $time
        Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -RunLevel Highest -Force
        Write-Host "Scheduled task '$taskName' registered to run daily at $time" -ForegroundColor Green
    } catch {
        Write-Error "Failed to register scheduled task: $_`nYou may need to run PowerShell as Administrator." -ErrorAction Stop
    }
}

if ($RunNow) {
    Run-Backup
}

if ($RegisterDaily) {
    Register-DailyTask -taskName $TaskName -time $Time
}

if (-not $RunNow -and -not $RegisterDaily) {
    Write-Host "No action specified. Use -RunNow to run backup or -RegisterDaily to create a daily scheduled task." -ForegroundColor Yellow
}
