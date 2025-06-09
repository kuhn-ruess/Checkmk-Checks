# DSS Monitor GPU Performance
# Load the necessary assembly for GPU information
Add-Type -AssemblyName System.Management

# Predefinitions
$Status = "P"
$StatusText = "normal"
$3D = 0
$Copy = 0
$VideoProcessing = 0
$VideoDecode = 0

# Function to get GPU usage and stores it into Array
function Get-GPUUsage {
    $gpuUsage = Get-WmiObject -Query "SELECT * FROM Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine"
    $gpuUsage | ForEach-Object {
    #$gpuUsage | Where-Object { $_.UtilizationPercentage -gt 0 } | ForEach-Object {
        [PSCustomObject]@{
            Name = $_.Name
            UtilizationPercentage = $_.UtilizationPercentage
        }
    }
}

# Main script
$gpuData = Get-GPUUsage

for ($i = 0; $i -lt $gpuData.Length; $i++) {
    if ( $gpuData[$i].UtilizationPercentage -gt 0 ) {
        # DEBUG Write-Output("Name=" + $gpuData[$i])
        if ( $gpuData[$i].Name.indexof("_3D") -gt 0 ) { $3D = $($gpuData[$i].UtilizationPercentage) }
        if ( $gpuData[$i].Name.indexof("_Copy") -gt 0 ) { $Copy = $($gpuData[$i].UtilizationPercentage) }
        if ( $gpuData[$i].Name.indexof("_VideoProcessing") -gt 0 ) { $VideoProcessing = $($gpuData[$i].UtilizationPercentage) }
        if ( $gpuData[$i].Name.indexof("_VideoDecode") -gt 0 ) { $VideoDecode = $($gpuData[$i].UtilizationPercentage) }
    }
}

# {0|1|2} CheckNameNoSpace {PerformanceData} message (!) means WARNING SYMBOL (!!) means CRITICAL SYMBOL   - varname=value;warn;crit;min;max
#Write-Output ("$Status DSS_GPU_Load 3D=$3D;80;90|Copy=$Copy;80;90|VideoProcessing=$VideoProcessing;80;90|VideoDecode=$VideoDecode;80;90 $StatusText")
#Write-Output ("--------")
Write-Output ("<<<digitals_signage:sep(124)>>>")
Write-Output ("GPU_Load 3D|$3D")
Write-Output ("GPU_Load Copy|$Copy")
Write-Output ("GPU_Load VideoProcessing|$VideoProcessing")
Write-Output ("GPU_Load VideoDecode|$VideoDecode")
