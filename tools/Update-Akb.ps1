[CmdletBinding()]
param(
    [string]$Msys2Root = $(if ($env:MSYS2_ROOT) { $env:MSYS2_ROOT } else { "C:\msys64" }),
    [string]$Python = "python",
    [switch]$SkipDatabaseRefresh,
    [switch]$SkipDeepInventory,
    [switch]$SkipRuntimeObservation,
    [ValidateSet("msys", "ucrt64", "clang64", "clangarm64", "mingw64", "mingw32")]
    [string]$RuntimeEnvironment = "msys",
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

if (-not $SkipRuntimeObservation) {
    $runtimeObservation = Join-Path $root "work\runtime-observation.json"
    & $Python (Join-Path $PSScriptRoot "collect_runtime_observation.py") `
        --environment $RuntimeEnvironment `
        --output $runtimeObservation
    if ($LASTEXITCODE -ne 0) { throw "Runtime observation collection failed." }

    & $Python (Join-Path $PSScriptRoot "import_runtime_observation.py") $runtimeObservation
    if ($LASTEXITCODE -ne 0) { throw "Runtime observation import failed." }
}

& $Python (Join-Path $PSScriptRoot "akb.py") all
if ($LASTEXITCODE -ne 0) { throw "AKB validation or generation failed." }

# Keep this list in step with the "Verify generated indexes are reproducible"
# step in .github/workflows/validate.yml. CI regenerates all of these and then
# runs `git diff --exit-code`, so a refresh that skips one leaves the working
# tree in a state CI rejects.
foreach ($generator in @("build_explorer.py", "build_diagrams.py", "build_object_diagrams.py", "build_catalog_views.py", "assess_akb_coverage.py")) {
    & $Python (Join-Path $PSScriptRoot $generator)
    if ($LASTEXITCODE -ne 0) { throw "$generator failed." }
}

Write-Host "MSYS2 Architecture Knowledge Base refresh completed."
