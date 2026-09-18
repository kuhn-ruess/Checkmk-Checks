# Aruba Central access point data via cencli
#
# Kuhn & Rueß GmbH
# Consulting and Development
# https://kuhn-ruess.de

$ErrorActionPreference = "Continue"

# UTF-8 for the cencli output we read and for the sections we write.
try { [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false) } catch { }

$ConfDir = if ($env:MK_CONFDIR) { $env:MK_CONFDIR } else { "C:\ProgramData\checkmk\agent\config" }
$TempDir = if ($env:TEMP) { $env:TEMP } else { [System.IO.Path]::GetTempPath() }

function Read-Config {
    <# Read the config file the bakery writes, KEY=VALUE per line. #>
    $config = @{}
    $file = Join-Path $ConfDir "aruba_central.cfg"
    if (Test-Path $file) {
        foreach ($line in (Get-Content $file -ErrorAction SilentlyContinue)) {
            $key, $value = $line.Trim().Split("=", 2)
            if ($value -and -not $key.StartsWith("#")) {
                $config[$key.Trim()] = $value.Trim().Trim('"').Trim("'")
            }
        }
    }
    return $config
}

$Cencli = (Read-Config)["CENCLI"]
if (-not $Cencli) { $Cencli = "cencli" }

function Invoke-Cencli {
    <# Run cencli and return its exit code, stdout and stderr. #>
    # cencli is a Python program, this pins its output encoding to the one we read with.
    $env:PYTHONIOENCODING = "utf-8"

    $errFile = Join-Path $TempDir "aruba_central_cencli.err"
    $out = & $Cencli show aps -v --json 2> $errFile | Out-String -Width 65535
    $code = $LASTEXITCODE

    $err = ""
    if (Test-Path $errFile) {
        $err = Get-Content $errFile -Raw
        Remove-Item $errFile -ErrorAction SilentlyContinue
    }

    return @{ ExitCode = $code; Stdout = [string]$out; Stderr = [string]$err }
}

function Find-Json {
    <# The JSON document cencli prints between its status lines. #>
    param([string]$Text)

    $start = $Text.IndexOf("{")
    $end = $Text.LastIndexOf("}")
    if ($start -lt 0 -or $end -lt $start) { return $null }

    try {
        return $Text.Substring($start, $end - $start + 1) | ConvertFrom-Json
    } catch {
        return $null
    }
}

function Get-Status {
    <# Pick the AP counts and the API rate limit out of the status lines. #>
    param([string]$Text)

    $status = [ordered]@{}

    if ($Text -match "ap:\s*(\d+)\s*\((\d+):(\d+)\)") {
        $status["aps_total"] = [int]$Matches[1]
        $status["aps_up"] = [int]$Matches[2]
        $status["aps_down"] = [int]$Matches[3]
    }
    if ($Text -match "clients:\s*(\d+)") {
        $status["clients"] = [int]$Matches[1]
    }
    if ($Text -match "API Rate Limit:\s*(\d+)\s+of\s+(\d+)\s+remaining") {
        $status["rate_remaining"] = [int]$Matches[1]
        $status["rate_limit"] = [int]$Matches[2]
    }

    return $status
}

function Get-ApHostName {
    <# The AP name, or its serial when the name is just the MAC address. #>
    param([string]$Name, $Ap)

    if ($Ap.mac -and $Name.Trim().ToLower() -eq ([string]$Ap.mac).Trim().ToLower() -and $Ap.serial) {
        return [string]$Ap.serial
    }
    return $Name
}

$output = Invoke-Cencli

# cencli mixes its status lines into both streams, the JSON is on one of them
$status = Get-Status -Text ($output.Stdout + $output.Stderr)
$aps = Find-Json -Text $output.Stdout
if ($null -eq $aps) { $aps = Find-Json -Text $output.Stderr }
if ($null -eq $aps) {
    $status["error"] = if ($null -eq $output.ExitCode) {
        "cencli could not be started"
    } else {
        "no JSON in the output of cencli (exit code $($output.ExitCode))"
    }
}

Write-Output "<<<aruba_central:sep(0)>>>"
Write-Output ($status | ConvertTo-Json -Compress)

if ($null -ne $aps) {
    foreach ($property in @($aps.PSObject.Properties | Sort-Object Name)) {
        $ap = $property.Value
        if ($null -eq $ap) { continue }
        if (-not $ap.PSObject.Properties["name"]) {
            $ap | Add-Member -NotePropertyName name -NotePropertyValue $property.Name
        }
        Write-Output ("<<<<" + (Get-ApHostName -Name $property.Name -Ap $ap) + ">>>>")
        Write-Output "<<<aruba_ap:sep(0)>>>"
        Write-Output ($ap | ConvertTo-Json -Depth 10 -Compress)
        Write-Output "<<<<>>>>"
    }
}
