<#
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

check_ping.ps1 - MRPE (Nagios) compatible ping check for Checkmk on Windows.

Usage (MRPE):
    check Ping_MyHost = powershell.exe -ExecutionPolicy Bypass -File C:\ProgramData\checkmk\agent\local\check_ping.ps1 myhost.example.com

Arguments:
    -HostName     Target hostname or IP (required, positional)
    -Count        Number of echo requests (default: 4)
    -WarningRta   WARN if average rta >= value in ms (default: 200)
    -CriticalRta  CRIT if average rta >= value in ms (default: 500)
    -WarningPl    WARN if packet loss >= value in %  (default: 40)
    -CriticalPl   CRIT if packet loss >= value in %  (default: 80)

Exit codes follow the Nagios convention: 0=OK, 1=WARN, 2=CRIT, 3=UNKNOWN.
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$HostName,
    [int]$Count = 4,
    [int]$WarningRta = 200,
    [int]$CriticalRta = 500,
    [int]$WarningPl = 40,
    [int]$CriticalPl = 80
)

$OK = 0
$WARN = 1
$CRIT = 2
$UNKNOWN = 3

if ([string]::IsNullOrWhiteSpace($HostName)) {
    Write-Host "PING UNKNOWN - no hostname given"
    exit $UNKNOWN
}

try {
    $pings = @(Test-Connection -ComputerName $HostName -Count $Count -ErrorAction Stop)
} catch {
    Write-Host "PING CRITICAL - $HostName not reachable: $($_.Exception.Message)"
    exit $CRIT
}

$received = $pings.Count
$sent = $Count
if ($sent -le 0) { $sent = 1 }
$lost = $sent - $received
$pl = [int][math]::Round(($lost / $sent) * 100)

if ($received -eq 0) {
    Write-Host "PING CRITICAL - 100% packet loss to $HostName | rta=U;$WarningRta;$CriticalRta;0; pl=100%;$WarningPl;$CriticalPl;0;100"
    exit $CRIT
}

$rtas = foreach ($p in $pings) {
    if ($null -ne $p.Latency) { $p.Latency }
    elseif ($null -ne $p.ResponseTime) { $p.ResponseTime }
    else { 0 }
}

$measured = $rtas | Measure-Object -Average -Minimum -Maximum
$rta_avg = [math]::Round($measured.Average, 2)
$rta_min = [math]::Round($measured.Minimum, 2)
$rta_max = [math]::Round($measured.Maximum, 2)

$state = $OK
$stateText = "OK"
if ($pl -ge $CriticalPl -or $rta_avg -ge $CriticalRta) {
    $state = $CRIT
    $stateText = "CRITICAL"
} elseif ($pl -ge $WarningPl -or $rta_avg -ge $WarningRta) {
    $state = $WARN
    $stateText = "WARNING"
}

$perf = "rta=${rta_avg}ms;${WarningRta};${CriticalRta};0; pl=${pl}%;${WarningPl};${CriticalPl};0;100 rtmin=${rta_min}ms rtmax=${rta_max}ms"
Write-Host "PING $stateText - $HostName: rta ${rta_avg}ms, lost ${pl}% ($received/$sent) | $perf"
exit $state
