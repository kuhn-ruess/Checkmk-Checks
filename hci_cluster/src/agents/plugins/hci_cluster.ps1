$CMK_VERSION = "2.0.0"
$MK_CONFDIR = $env:MK_CONFDIR

$CONFIG_FILE="${MK_CONFDIR}\hci_cluster.cfg.ps1"
if (test-path -path "${CONFIG_FILE}" ) {
     . "${CONFIG_FILE}"
} else {
    exit
}

$Clusters=get-cluster -Domain $domain -Name $cluster_filter

foreach ($Cluster in $Clusters){
    Write-Output  "<<<<$cluster>>>>"
    Write-Output "<<<hci_cluster_resources:sep(58)>>>"
    Get-ClusterResource -Cluster $Cluster | ? {$_.ResourceType -NotLike 'Virtual Machine*' -and $_.Name -notlike '*Cau*'}  | Format-List
    Write-Output  "<<<hci_cluster_nodes:sep(58)>>>"
    Get-ClusterNode -cluster $Cluster | Format-List
    Write-Output  "<<<hci_cluster_performance:sep(58)>>>"
    Invoke-Command -ComputerName $Cluster -ScriptBlock { Get-Cluster | Get-ClusterPerf | Format-List }

    $Node = (get-clusternode -Cluster $Cluster | ? State -eq 'Up')[0]

    Invoke-Command -ComputerName $Node.Name -ScriptBlock {
        Write-Output "<<<hci_storage_pools:sep(58)>>>"
        Get-StoragePool -FriendlyName '*S2D*'  | Format-List
        Write-Output  "<<<hci_storage_jobs:sep(58)>>>"
        Get-StorageJob  | ? Name -like '*Repair'  | Format-List
        Write-Output "<<<hci_virtual_disks:sep(58)>>>"
        Get-VirtualDisk  | Format-List
        Write-Output  "<<<hci_s2d_storage_pools:sep(58)>>>"
        get-storagepool -FriendlyName '*S2D*' | Get-PhysicalDisk | Format-List
    }
    Write-Output "<<<<>>>>"
}


foreach ($Cluster in $Clusters){
    $Nodes = (get-clusternode -Cluster $Cluster | ? State -eq 'Up')

    foreach ($Node in $Nodes){
        $NodeName = $Node.Name

        Write-Output  "<<<<$NodeName>>>>"

       Invoke-Command -ComputerName $Node.Name -ScriptBlock {
            Write-Output  "<<<hci_s2d_volume_performance:sep(58)>>>"
            Get-Volume -FriendlyName $using:NodeName | Get-ClusterPerf | Format-List 
        }
    }
}
Write-Output "<<<<>>>>"