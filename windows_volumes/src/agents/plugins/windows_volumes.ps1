# Kuhn & Rueß GmbH - Windows volumes (folder mount points)
# Emits one line per folder mounted volume for the Checkmk check "windows_volumes".
#
# Plain drive letters (C:\, D:\), raw volume GUID paths and volumes without a
# real filesystem / size (Recovery, EFI, ...) are filtered out, so only the
# volumes that are mounted into a folder are reported.

$ErrorActionPreference = "SilentlyContinue"

Write-Output "<<<windows_volumes:sep(124)>>>"

Get-Partition | ForEach-Object {
    $partition = $_
    $volume = $partition | Get-Volume
    if (-not $volume) { return }

    # Skip volumes without a usable filesystem or size (Recovery, EFI, ...).
    if (-not $volume.FileSystemType -or $volume.Size -le 0) { return }

    foreach ($path in $partition.AccessPaths) {
        # Skip plain drive letter roots ("C:\") and raw volume GUID paths.
        if ($path -match '^[A-Za-z]:\\$') { continue }
        if ($path -like '\\?\Volume*') { continue }

        $label = $volume.FileSystemLabel
        if (-not $label) { $label = $path }

        $line = @(
            $label,
            $volume.HealthStatus,
            $volume.OperationalStatus,
            $volume.Size,
            $volume.SizeRemaining,
            $volume.FileSystemType,
            $path
        ) -join "|"

        Write-Output $line
    }
}
