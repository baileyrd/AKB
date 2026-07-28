[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$TaskName = "MSYS2 Architecture Knowledge Base Refresh",
    [string]$DailyAt = "03:00",
    [string]$Msys2Root = $(if ($env:MSYS2_ROOT) { $env:MSYS2_ROOT } else { "C:\msys64" })
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$updateScript = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot "Update-Akb.ps1"))
$powerShell = (Get-Command pwsh.exe -ErrorAction Stop).Source
$at = [DateTime]::ParseExact($DailyAt, "HH:mm", [Globalization.CultureInfo]::InvariantCulture)
$argument = "-NoProfile -File `"$updateScript`" -Msys2Root `"$Msys2Root`""
$action = New-ScheduledTaskAction -Execute $powerShell -Argument $argument
$trigger = New-ScheduledTaskTrigger -Daily -At $at
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew

if ($PSCmdlet.ShouldProcess($TaskName, "Register daily AKB refresh at $DailyAt")) {
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description "Refresh the evidence-backed MSYS2 Architecture Knowledge Base." `
        -Force | Out-Null
    Write-Host "Registered '$TaskName' to run daily at $DailyAt."
}
