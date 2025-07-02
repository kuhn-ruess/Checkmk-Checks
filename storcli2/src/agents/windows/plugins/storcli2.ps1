<#
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
#>

$CMD_VERSION = "2.3.0p34"

$MK_CONFDIR = $env:MK_CONFDIR
if (!$MK_CONFDIR) {
    $MK_CONFDIR = "${env:ProgramData}\checkmk\agent\config"
}

$CONFIG_FILE = "${MK_CONFDIR}\storcli2.ps1"
if (Test-Path -Path "$CONFIG_FILE") {
    . "$CONFIG_FILE"
}

function rewriteOutput($output) {
    foreach($line in $output) {
        if ($line[-1] -eq ":") {
            Write-Host "<<<storcli2_$($line.substring(0, $line.Length-2).ToLower().replace(' ', '_').replace('/', '_').replace('.', ''))>>>"
        } elseif ($line[0] -eq "=" -and $line[-1] -eq "=") {
            # Ignore section separator
            continue
        } elseif (
            $line.Contains("Drive Groups") -or
            $line.Contains("Virtual Drives") -or
            $line.Contains("Physical Drives") -or
            $line.Contains("Enclosures")) {
            # Ignore summary lines in wrong sections
            continue
        } elseif ($line.Contains("|") -or ($line.Split(" ").Length -eq 1 -and $line[0] -ne "-")) {
            # Ignore state description
            continue
        } else {
            Write-Host $line
        }
    }
}

Write-Host "<<<storcli2_tool>>>"

if (Test-Path -Path $STORCLI2_PATH) {
    rewriteOutput(@(& $STORCLI2_PATH /call show all))
    exit
}

if (Get-Command "StorCLI2.exe" -ErrorAction SilentlyContinue) {
    rewriteOutput(@(& StorCLI2.exr /call show all))
    exit
}

Write-Host "ERROR: StorCLI2.exe was not found in: "
Write-Host "- $($STORCLI2_PATH) (configured path)"
Write-Host "- system path"
