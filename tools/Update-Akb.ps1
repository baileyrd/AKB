[CmdletBinding()]
param(
    [string]$Msys2Root = $(if ($env:MSYS2_ROOT) { $env:MSYS2_ROOT } else { "C:\msys64" }),
    [string]$Python = "python",
    [switch]$SkipDatabaseRefresh,
    [switch]$SkipDeepInventory,
    [ValidateSet("installed", "repositories")]
    [string]$InventoryScope = "installed",
    [string]$RecipeRoot = ""
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

if (-not $SkipDeepInventory) {
    $inventoryDirectory = Join-Path $root "work\inventory"
    $collectorArguments = @{
        Msys2Root = $Msys2Root
        Python = $Python
        Scope = $InventoryScope
        OutputDirectory = $inventoryDirectory
        SkipFileDatabaseRefresh = $SkipDatabaseRefresh
    }
    if ($RecipeRoot) {
        $collectorArguments["RecipeRoot"] = $RecipeRoot
    }
    & (Join-Path $PSScriptRoot "Collect-AkbDeepInventory.ps1") @collectorArguments
    if ($LASTEXITCODE -ne 0) { throw "Deep inventory collection failed." }

    & $Python (Join-Path $PSScriptRoot "import_deep_inventory.py") $inventoryDirectory
    if ($LASTEXITCODE -ne 0) { throw "Deep inventory import failed." }
}

& $Python (Join-Path $PSScriptRoot "akb.py") all
if ($LASTEXITCODE -ne 0) { throw "AKB validation or generation failed." }

Write-Host "MSYS2 Architecture Knowledge Base refresh completed."
