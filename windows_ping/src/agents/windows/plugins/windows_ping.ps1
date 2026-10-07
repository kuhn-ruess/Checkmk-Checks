<#
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

windows_ping.ps1: Checkmk agent plug-in for Windows.

Pings all targets from windows_ping.cfg.ps1 (written by the agent bakery rule
"Windows Ping") concurrently and prints one local check per target.
#>

$Targets   = @()
$Count     = 1
$TimeoutMs = 1000
$WarnRta   = 100
$CritRta   = 500
$WarnPl    = 40
$CritPl    = 80

$ConfigDir = $env:MK_CONFDIR
if (-not $ConfigDir) { $ConfigDir = Join-Path $env:ProgramData 'checkmk\agent\config' }
$ConfigFile = Join-Path $ConfigDir 'windows_ping.cfg.ps1'
if (Test-Path -Path $ConfigFile) {
    . $ConfigFile
}

if (-not $Targets -or $Targets.Count -eq 0) {
    exit 0
}
if ($Count -lt 1) { $Count = 1 }

$stats = foreach ($target in $Targets) {
    $name = $target.Name
    if ([string]::IsNullOrWhiteSpace($name)) { $name = $target.Address }
    [pscustomobject]@{
        Address  = $target.Address
        Service  = ('Ping ' + $name) -replace '"', ''
        Rtts     = New-Object System.Collections.Generic.List[double]
        LastFail = $null
    }
}

for ($round = 0; $round -lt $Count; $round++) {
    $pending = foreach ($stat in $stats) {
        $ping = New-Object System.Net.NetworkInformation.Ping
        try {
            $task = $ping.SendPingAsync($stat.Address, $TimeoutMs)
        } catch {
            $task = $null
            $stat.LastFail = $_.Exception.Message
        }
        [pscustomobject]@{ Stat = $stat; Ping = $ping; Task = $task }
    }

    foreach ($item in $pending) {
        if ($null -ne $item.Task) {
            try {
                $reply = $item.Task.GetAwaiter().GetResult()
                if ($reply.Status -eq 'Success') {
                    $item.Stat.Rtts.Add([double]$reply.RoundtripTime)
                } else {
                    $item.Stat.LastFail = [string]$reply.Status
                }
            } catch {
                $err = $_.Exception
                while ($null -ne $err.InnerException) { $err = $err.InnerException }
                $item.Stat.LastFail = $err.Message
            }
        }
        $item.Ping.Dispose()
    }
}

function Format-Level($value) {
    if ($null -eq $value) { return '' }
    return ([double]$value).ToString('0.###', [System.Globalization.CultureInfo]::InvariantCulture)
}

function Format-Seconds($ms) {
    if ($null -eq $ms) { return '' }
    return ([double]$ms / 1000).ToString('0.######', [System.Globalization.CultureInfo]::InvariantCulture)
}

"<<<local:sep(0)>>>"

foreach ($stat in $stats) {
    $received = $stat.Rtts.Count
    $loss = [int][math]::Round((($Count - $received) / $Count) * 100)
    $plPerf = "pl=$loss;$(Format-Level $WarnPl);$(Format-Level $CritPl);0;100"

    if ($received -eq 0) {
        "2 `"$($stat.Service)`" $plPerf $($stat.Address): no reply ($($stat.LastFail)), packet loss 100%"
        continue
    }

    $rta = ($stat.Rtts | Measure-Object -Average).Average
    $rtaText = [math]::Round($rta, 2).ToString([System.Globalization.CultureInfo]::InvariantCulture)
    $rtaPerf = "rta=$(Format-Seconds $rta);$(Format-Seconds $WarnRta);$(Format-Seconds $CritRta);0"

    $state = 0
    $notes = @()
    if ($null -ne $CritRta -and $rta -ge $CritRta) {
        $state = 2; $notes += "rta >= $CritRta ms"
    } elseif ($null -ne $WarnRta -and $rta -ge $WarnRta) {
        $state = 1; $notes += "rta >= $WarnRta ms"
    }
    if ($null -ne $CritPl -and $loss -ge $CritPl) {
        $state = 2; $notes += "loss >= $CritPl%"
    } elseif ($null -ne $WarnPl -and $loss -ge $WarnPl) {
        if ($state -lt 1) { $state = 1 }
        $notes += "loss >= $WarnPl%"
    }

    $text = "$($stat.Address): rta $rtaText ms, packet loss $loss% ($received/$Count)"
    if ($notes.Count -gt 0) { $text += " (" + ($notes -join ', ') + ")" }
    "$state `"$($stat.Service)`" $rtaPerf|$plPerf $text"
}
