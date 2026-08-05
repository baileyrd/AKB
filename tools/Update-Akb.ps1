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

# Fail here, with the fix in the message, rather than several steps later with
# a misleading one. On a Windows host with no Python installed, `python`
# resolves to the Microsoft Store alias stub, which prints its own advice and
# exits 9009 — which this script would otherwise report as "Package catalog
# import failed." The repository's own documentation uses `py -3`.
& $Python --version 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "'$Python' is not a working Python interpreter (exit $LASTEXITCODE). On Windows, pass -Python py, or install Python and put it on PATH."
}

# Say which installation is being read before doing any work. A host with more
# than one MSYS2 tree is the normal case here, not an edge case — Volumes 3 and
# 7 record three distinct installations — and the default root may exist while
# holding empty sync databases, which fails much later and much less clearly.
$pacmanPath = Join-Path $Msys2Root "usr\bin\pacman.exe"
if (-not (Test-Path -LiteralPath $pacmanPath -PathType Leaf)) {
    throw "pacman.exe was not found at '$pacmanPath'. Pass -Msys2Root <path> or set MSYS2_ROOT."
}
Write-Host "Reading MSYS2 installation at $Msys2Root"

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

    # --accumulate, because the projection holds evidence this run cannot
    # reproduce. model/inventory/current.json is three accumulated
    # package-archive snapshots — downloaded payloads for zlib, curl, and
    # zstd, analysed byte by byte. A refresh here collects scope=installed
    # through pacman, which is a different modality, not a newer version of
    # the same observation. Without this flag the refresh would discard 552
    # entities and the evidence record two documentation pages cite, and
    # `akb.py validate-docs` would then fail on a tree the operator has no
    # obvious way to repair.
    & $Python (Join-Path $PSScriptRoot "import_deep_inventory.py") $inventoryDirectory --accumulate
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
foreach ($generator in @("build_explorer.py", "build_diagrams.py", "build_object_diagrams.py", "build_object_facts.py", "build_volume_ledger.py", "build_catalog_views.py", "assess_akb_coverage.py")) {
    & $Python (Join-Path $PSScriptRoot $generator)
    if ($LASTEXITCODE -ne 0) { throw "$generator failed." }
}

Write-Host "MSYS2 Architecture Knowledge Base refresh completed."
