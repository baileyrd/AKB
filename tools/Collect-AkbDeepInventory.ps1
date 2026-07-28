[CmdletBinding()]
param(
    [string]$Msys2Root = $(if ($env:MSYS2_ROOT) { $env:MSYS2_ROOT } else { "C:\msys64" }),
    [string]$Python = "python",
    [ValidateSet("installed", "repositories")]
    [string]$Scope = "installed",
    [switch]$SkipFileDatabaseRefresh,
    [string]$RecipeRoot = "",
    [string]$OutputDirectory = (Join-Path $PSScriptRoot "..\work\inventory")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if ($Scope -eq "repositories" -and -not $SkipFileDatabaseRefresh) {
    $pacman = Join-Path $Msys2Root "usr\bin\pacman.exe"
    if (-not (Test-Path -LiteralPath $pacman -PathType Leaf)) {
        throw "pacman.exe was not found at '$pacman'."
    }
    & $pacman -Fy --noconfirm
    if ($LASTEXITCODE -ne 0) {
        throw "pacman file-database refresh failed."
    }
}

$arguments = @(
    (Join-Path $PSScriptRoot "deep_inventory.py"),
    "--msys2-root", $Msys2Root,
    "--output", $OutputDirectory,
    "--scope", $Scope
)
if ($RecipeRoot) {
    $arguments += @("--recipes", $RecipeRoot)
}
& $Python @arguments
if ($LASTEXITCODE -ne 0) {
    throw "Deep inventory collection failed."
}
