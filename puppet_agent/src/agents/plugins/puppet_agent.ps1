# Writen to conform to the output of the linux plugin from 
# https://github.com/allangood/check_mk/tree/master/plugins/puppet
# Contribution from: https://github.com/jeff-cook

# requires puppet 7+
$lastrun = "C:\ProgramData\PuppetLabs\puppet\public\last_run_summary.yaml"
if (Test-Path $lastrun) {
  Write-Output "<<<puppet_agent>>>"
  $content = Get-Content $lastrun
  $content = $content -replace “  ”,””
  $content | Select-String -Pattern “last_run:” | %{$_ -replace “  ”,””}
  $content | Select-String -Pattern “resources:” -Context 0,8 | %{$_ -replace “> ”,””} | %{$_ -replace “  ”,”resources_”}
  $content | Select-String -Pattern “events:” -Context 0,3 | %{$_ -replace “> ”,””} | %{$_ -replace “  ”,”events_”}
}
#Else {Write-Output "no file found"}
