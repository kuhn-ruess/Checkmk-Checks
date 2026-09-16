# Aruba Central access point data via cencli
#
# Kuhn & Rueß GmbH
# Consulting and Development
# https://kuhn-ruess.de

$ErrorActionPreference = "Continue"

$Cencli = if ($env:ARUBA_CENCLI) { $env:ARUBA_CENCLI } else { "cencli" }
$TempDir = if ($env:TEMP) { $env:TEMP } else { [System.IO.Path]::GetTempPath() }
$ErrorFile = Join-Path $TempDir "aruba_central_cencli.err"

function Get-CencliOutput {
    <# Run cencli and return its exit code, stdout and stderr. #>
    $out = & $Cencli show aps -v --json 2> $ErrorFile | Out-String
    $code = $LASTEXITCODE
    $err = ""
    if (Test-Path $ErrorFile) {
        $err = Get-Content $ErrorFile -Raw -ErrorAction SilentlyContinue
        Remove-Item $ErrorFile -ErrorAction SilentlyContinue
    }
    return @{ ExitCode = $code; Stdout = $out; Stderr = $err }
}

function Split-Json {
    <# Split the JSON document from the status lines cencli mixes into its output. #>
    param([string]$Text)

    $start = $Text.IndexOf("{")
    $end = $Text.LastIndexOf("}")
    if ($start -lt 0 -or $end -lt $start) {
        return @{ Data = $null; Rest = $Text }
    }

    try {
        $data = $Text.Substring($start, $end - $start + 1) | ConvertFrom-Json
    } catch {
        return @{ Data = $null; Rest = $Text }
    }

    return @{ Data = $data; Rest = $Text.Substring(0, $start) + $Text.Substring($end + 1) }
}

function Get-Status {
    <# Pick the AP counts and the API rate limit out of the remaining output. #>
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

$output = Get-CencliOutput
$parsed = Split-Json -Text $output.Stdout
if ($null -eq $parsed.Data) {
    $parsed = Split-Json -Text $output.Stderr
    $rest = $output.Stdout + $parsed.Rest
} else {
    $rest = $parsed.Rest + $output.Stderr
}

$aps = $parsed.Data
$status = Get-Status -Text $rest
if ($null -eq $aps) {
    $status["error"] = if ($null -ne $output.ExitCode) {
        "no JSON in the output of cencli (exit code $($output.ExitCode))"
    } else {
        "cencli could not be started"
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
