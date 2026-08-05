[CmdletBinding()]
param(
    [string]$Msys2Root = $(if ($env:MSYS2_ROOT) { $env:MSYS2_ROOT } else { "C:\msys64" }),
    [string]$OutputDirectory = (Join-Path $PSScriptRoot "..\work\catalog"),
    [switch]$SkipDatabaseRefresh
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-Pacman {
    param(
        [Parameter(Mandatory)][string[]]$Arguments,
        # Queries that must return rows. pacman exits 0 with no output when the
        # sync databases are empty, so an exit-code check alone lets an empty
        # result travel until something downstream fails on a parameter that
        # has nothing to do with the cause. A host with two MSYS2 installations
        # hits this: the root that is found first has pacman.exe but no synced
        # databases, and the reported error named a `Lines` parameter ninety
        # lines away from the real problem.
        [switch]$AllowEmpty
    )

    $oldLang = $env:LANG
    $oldLcAll = $env:LC_ALL
    try {
        $env:LANG = "C"
        $env:LC_ALL = "C"
        $output = & $script:Pacman @Arguments 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "pacman $($Arguments -join ' ') failed with exit code $LASTEXITCODE`n$($output -join [Environment]::NewLine)"
        }
        $lines = @($output | ForEach-Object { "$_" })
        # Count only non-blank lines, but return every line. ConvertFrom-PacmanInfo
        # uses blank lines as its record separator, so filtering them here would
        # merge every package into a single record.
        $substantive = @($lines | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }).Count
        if (-not $AllowEmpty -and $substantive -eq 0) {
            throw @"
pacman $($Arguments -join ' ') produced no output at '$script:Pacman' and exited 0.

That normally means this installation's sync databases are empty, not that the
ecosystem has no packages. Check which installation is being read:

    & '$script:Pacman' -Sl | Measure-Object -Line

If that is also empty, refresh the databases:

    & '$script:Pacman' -Syy --noconfirm

If a different MSYS2 installation is the one you meant, pass it explicitly:

    -Msys2Root <path>    (or set the MSYS2_ROOT environment variable)
"@
        }
        return $lines
    }
    finally {
        $env:LANG = $oldLang
        $env:LC_ALL = $oldLcAll
    }
}

function ConvertFrom-PacmanInfo {
    param([Parameter(Mandatory)][string[]]$Lines)

    $records = [System.Collections.Generic.List[hashtable]]::new()
    $record = [ordered]@{}
    $currentKey = $null

    foreach ($line in $Lines) {
        if ([string]::IsNullOrWhiteSpace($line)) {
            if ($record.Contains("Name")) {
                $records.Add($record)
            }
            $record = [ordered]@{}
            $currentKey = $null
            continue
        }

        if ($line -match '^([^:]+?)\s*:\s?(.*)$') {
            $currentKey = $Matches[1].Trim()
            $record[$currentKey] = $Matches[2].Trim()
        }
        elseif ($currentKey) {
            $record[$currentKey] = "$($record[$currentKey])`n$($line.Trim())".Trim()
        }
    }

    if ($record.Contains("Name")) {
        $records.Add($record)
    }
    return $records
}

function Split-PacmanOptionalDependencies {
    param([AllowNull()][string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value) -or $Value -eq "None") {
        return @()
    }
    $results = [System.Collections.Generic.List[string]]::new()
    foreach ($line in ($Value -split "`r?`n")) {
        $candidate = $line.Trim()
        if ($candidate -match '^([A-Za-z0-9@._+-]+(?:[<>=]+[^\s:]+)?)') {
            $results.Add($Matches[1])
        }
    }
    return $results
}

function Split-PacmanList {
    param([AllowNull()][string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value) -or $Value -eq "None") {
        return @()
    }
    return @($Value -split '\s+' | Where-Object { $_ -and $_ -ne "None" })
}

function Get-DependencyName {
    param([Parameter(Mandatory)][string]$Value)
    $withoutDescription = ($Value -split ':\s', 2)[0]
    return ($withoutDescription -replace '([<>=].*)$', '').Trim()
}

function Get-Classification {
    param([string]$Repository, [string]$Name)
    if ($Name -match '-toolchain$') { return "toolchain-group" }
    if ($Name -match '^(mingw-w64-|msys2-runtime|filesystem|bash$|pacman$)') {
        if ($Name -match '^(mingw-w64-)') { return "mingw-package" }
        return "system-package"
    }
    if ($Repository -eq "msys") { return "msys-package" }
    return "native-package"
}

$script:Pacman = Join-Path $Msys2Root "usr\bin\pacman.exe"
if (-not (Test-Path -LiteralPath $script:Pacman -PathType Leaf)) {
    throw "pacman.exe was not found at '$script:Pacman'. Set -Msys2Root or MSYS2_ROOT."
}

$OutputDirectory = [IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null

if (-not $SkipDatabaseRefresh) {
    Invoke-Pacman -Arguments @("-Sy", "--noconfirm") -AllowEmpty | Out-Null
}

$installed = @{}
foreach ($line in (Invoke-Pacman -Arguments @("-Q"))) {
    if ($line -match '^(\S+)\s+(.+)$') {
        $installed[$Matches[1]] = $Matches[2]
    }
}

$syncRecords = ConvertFrom-PacmanInfo -Lines (Invoke-Pacman -Arguments @("-Si"))
$packages = [System.Collections.Generic.List[object]]::new()
$edges = [System.Collections.Generic.List[object]]::new()
$groups = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)

foreach ($item in $syncRecords) {
    $name = "$($item["Name"])"
    $repository = "$($item["Repository"])".ToLowerInvariant()
    $isInstalled = $installed.ContainsKey($name)
    $required = @(Split-PacmanList $item["Depends On"])
    $optional = @(Split-PacmanOptionalDependencies $item["Optional Deps"])

    foreach ($group in (Split-PacmanList $item["Groups"])) {
        [void]$groups.Add($group)
    }

    foreach ($dependency in $required) {
        $target = Get-DependencyName $dependency
        if ($target) {
            $edges.Add([pscustomobject][ordered]@{
                source_repository = $repository
                source_package = $name
                relationship = "runtime-depends-on"
                target_package = $target
                constraint = $dependency.Substring($target.Length)
            })
        }
    }
    foreach ($dependency in $optional) {
        $target = Get-DependencyName $dependency
        if ($target) {
            $edges.Add([pscustomobject][ordered]@{
                source_repository = $repository
                source_package = $name
                relationship = "optional-depends-on"
                target_package = $target
                constraint = ""
            })
        }
    }

    $packages.Add([pscustomobject][ordered]@{
        repository = $repository
        name = $name
        version = "$($item["Version"])"
        installed = $isInstalled
        installed_version = $(if ($isInstalled) { $installed[$name] } else { "" })
        architecture = "$($item["Architecture"])"
        classification = Get-Classification -Repository $repository -Name $name
        description = "$($item["Description"])"
        groups = (Split-PacmanList $item["Groups"]) -join ";"
        licenses = (Split-PacmanList $item["Licenses"]) -join ";"
        project_url = "$($item["URL"])"
        required_dependencies = $required -join ";"
        optional_dependencies = $optional -join ";"
        provides = (Split-PacmanList $item["Provides"]) -join ";"
        conflicts = (Split-PacmanList $item["Conflicts With"]) -join ";"
        replaces = (Split-PacmanList $item["Replaces"]) -join ";"
        download_size = "$($item["Download Size"])"
        installed_size = "$($item["Installed Size"])"
        build_date = "$($item["Build Date"])"
    })
}

$packages = @($packages | Sort-Object repository, name)
$edges = @($edges | Sort-Object source_package, relationship, target_package -Unique)
$allPackagesPath = Join-Path $OutputDirectory "all-packages.csv"
$edgePath = Join-Path $OutputDirectory "dependency-edges.csv"
$installedPath = Join-Path $OutputDirectory "installed-packages.csv"

$packages | Export-Csv -LiteralPath $allPackagesPath -NoTypeInformation -Encoding utf8
$edges | Export-Csv -LiteralPath $edgePath -NoTypeInformation -Encoding utf8
$packages | Where-Object installed | Export-Csv -LiteralPath $installedPath -NoTypeInformation -Encoding utf8

$repositories = @($packages.repository | Sort-Object -Unique)
foreach ($repository in $repositories) {
    $packages |
        Where-Object repository -eq $repository |
        Export-Csv -LiteralPath (Join-Path $OutputDirectory "$repository-packages.csv") -NoTypeInformation -Encoding utf8
}

@($groups | Sort-Object) | Set-Content -LiteralPath (Join-Path $OutputDirectory "package-groups.txt") -Encoding utf8

$summary = @(
    "# MSYS2 Package Catalog Summary"
    ""
    "Generated: $(Get-Date -Format o)"
    ""
    "| Repository | Packages | Installed |"
    "| --- | ---: | ---: |"
)
foreach ($repository in $repositories) {
    $repoPackages = @($packages | Where-Object repository -eq $repository)
    $summary += "| $repository | $($repoPackages.Count) | $(@($repoPackages | Where-Object installed).Count) |"
}
$summary += ""
$summary += "Total packages: **$($packages.Count)**"
$summary += ""
$summary += "Dependency edges: **$($edges.Count)**"
$summary | Set-Content -LiteralPath (Join-Path $OutputDirectory "catalog-summary.md") -Encoding utf8

$hashInputs = @("all-packages.csv", "dependency-edges.csv", "installed-packages.csv", "package-groups.txt")
$hashes = [ordered]@{}
foreach ($file in $hashInputs) {
    $path = Join-Path $OutputDirectory $file
    $hashes[$file] = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}

$manifest = [ordered]@{
    schema_version = "1.0.0"
    generated_at = (Get-Date).ToUniversalTime().ToString("o")
    collector = "tools/catalog-msys2-packages.ps1"
    msys2_root = $Msys2Root
    pacman_version = ((Invoke-Pacman -Arguments @("--version")) -join " ")
    repositories = $repositories
    package_count = $packages.Count
    installed_count = @($packages | Where-Object installed).Count
    dependency_edge_count = $edges.Count
    sha256 = $hashes
}
$manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $OutputDirectory "catalog-manifest.json") -Encoding utf8

Write-Host "Cataloged $($packages.Count) packages and $($edges.Count) dependency edges from $($repositories.Count) repositories."
Write-Host "Output: $OutputDirectory"
