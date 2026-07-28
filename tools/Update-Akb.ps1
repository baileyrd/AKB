[CmdletBinding()]
param(
    [string]$Msys2Root = $(if ($env:MSYS2_ROOT) { $env:MSYS2_ROOT } else { "C:\msys64" }),
    [string]$Python = "python",
    [switch]$SkipDatabaseRefresh
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$catalogDirectory = Join-Path $root "work\catalog"

& (Join-Path $PSScriptRoot "catalog-msys2-packages.ps1") `
    -Msys2Root $Msys2Root `
    -OutputDirectory $catalogDirectory `
    -SkipDatabaseRefresh:$SkipDatabaseRefresh
if ($LASTEXITCODE -ne 0) { throw "Package catalog collection failed." }

& $Python (Join-Path $PSScriptRoot "import_package_catalog.py") $catalogDirectory
if ($LASTEXITCODE -ne 0) { throw "Package catalog import failed." }

& $Python (Join-Path $PSScriptRoot "akb.py") all
if ($LASTEXITCODE -ne 0) { throw "AKB validation or generation failed." }

Write-Host "MSYS2 Architecture Knowledge Base refresh completed."
