# Aruba Central access point data via cencli
#
# Kuhn & Rueß GmbH
# Consulting and Development
# https://kuhn-ruess.de

# Read by the agent for the <<<checkmk_agent_plugins_win>>> section, so that the
# agent output names the version of this plug-in.
$CMK_VERSION = "1.1.2"

$ErrorActionPreference = "Continue"

# UTF-8 for the cencli output we read and for the sections we write.
try { [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding $false } catch { }

# Written before anything else, so that Checkmk sees the section even when the
# agent kills the plug-in or PowerShell aborts it.
Write-Output "<<<aruba_central:sep(0)>>>"

$ConfDir = if ($env:MK_CONFDIR) { $env:MK_CONFDIR } else { "C:\ProgramData\checkmk\agent\config" }

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

$ConfigFile = Join-Path $ConfDir "aruba_central.cfg"
if (-not (Test-Path $ConfigFile)) { $ConfigFile = "" }

$Config = Read-Config
$Cencli = if ($Config["CENCLI"]) { $Config["CENCLI"] } else { "cencli" }
$Timeout = if ($Config["TIMEOUT"]) { [int]$Config["TIMEOUT"] } else { 300 }

function Invoke-Cencli {
    <# Run cencli and return its exit code, stdout and stderr. #>
    $info = New-Object System.Diagnostics.ProcessStartInfo
    $info.FileName = $Cencli
    $info.Arguments = "show aps -v --json"
    $info.UseShellExecute = $false
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    $info.StandardOutputEncoding = New-Object System.Text.UTF8Encoding $false
    $info.StandardErrorEncoding = New-Object System.Text.UTF8Encoding $false
    # cencli is a Python program, this pins its output encoding to the one we read with.
    $info.EnvironmentVariables["PYTHONIOENCODING"] = "utf-8"

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $info
    [void]$process.Start()

    # Both pipes are read before waiting, a full pipe buffer would block cencli.
    $stdout = $process.StandardOutput.ReadToEndAsync()
    $stderr = $process.StandardError.ReadToEndAsync()

    # Stopping a little before the agent does keeps the reason in the section.
    $budget = [Math]::Max(10, $Timeout - 15)
    if (-not $process.WaitForExit($budget * 1000)) {
        try { $process.Kill() } catch { }
        throw "cencli did not finish within $budget seconds"
    }

    return @{ ExitCode = $process.ExitCode; Stdout = $stdout.Result; Stderr = $stderr.Result }
}

function Get-Excerpt {
    <# The last lines of the cencli output, for the error message. #>
    param([string]$Text)

    $lines = @($Text -split '\r?\n' | ForEach-Object { $_.Trim() } | Where-Object { $_ })
    if ($lines.Count -eq 0) { return "" }

    $tail = ($lines[[Math]::Max(0, $lines.Count - 3)..($lines.Count - 1)]) -join " | "
    if ($tail.Length -gt 200) { $tail = $tail.Substring(0, 200) }
    return $tail
}

function Find-Json {
    <# The JSON document cencli prints between its status lines. #>
    param([string]$Text)

    $end = $Text.LastIndexOf("}")
    $start = $Text.IndexOf("{")

    # A stray brace in an error message may sit in front of the document.
    for ($attempt = 0; $attempt -lt 5 -and $start -ge 0 -and $start -lt $end; $attempt++) {
        try {
            return $Text.Substring($start, $end - $start + 1) | ConvertFrom-Json
        } catch {
            $start = $Text.IndexOf("{", $start + 1)
        }
    }
    return $null
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

$aps = $null

try {
    $output = Invoke-Cencli

    # cencli mixes its status lines into both streams, the JSON is on one of them
    $status = Get-Status -Text ($output.Stdout + $output.Stderr)
    $aps = Find-Json -Text $output.Stdout
    if ($null -eq $aps) { $aps = Find-Json -Text $output.Stderr }
    if ($null -eq $aps) {
        $excerpt = Get-Excerpt -Text $output.Stderr
        if (-not $excerpt) { $excerpt = Get-Excerpt -Text $output.Stdout }
        $status["error"] = "no JSON in the output of cencli " +
            "(exit code $($output.ExitCode)): $excerpt"
    }
} catch {
    $status = [ordered]@{}
    $status["error"] = "cencli failed: $($_.Exception.Message)"
}

# All of this is in the section so that the service can show which plug-in version
# ran, which cencli it called, as whom, with which budget and which config.
$status["version"] = $CMK_VERSION
$status["cencli"] = [string]$Cencli
$status["user"] = if ($env:USERNAME) { "$env:USERDOMAIN\$env:USERNAME" } else { "" }
$status["timeout"] = $Timeout
$status["config"] = [string]$ConfigFile

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
