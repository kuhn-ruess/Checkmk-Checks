# XFS Project Quotas

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.4.0p19-blue)
<!-- compatibility-badges:end -->

Monitors XFS project (directory) quotas on Linux. One service `XFS Quota on <project>`
per project with a block or inode limit, evaluated like the filesystem check: levels on
used or free space in percent or absolute, optional magic factor, growth trend and time
left until the quota is full, plus states for exceeded soft and reached hard limits.

## How it works

The agent plug-in `xfs_quota` (POSIX shell, runs as root) finds all mounted XFS
filesystems with project quota accounting (`prjquota`/`pquota` in `/proc/mounts`) and runs
`xfs_quota -x -c 'report -p -b -i -N'` on each. It writes one line per project:

```
<<<xfs_quota>>>
mountpoint:device:project:used:soft:hard:inodes_used:inodes_soft:inodes_hard
```

Block values are KiB (the unit of `xfs_quota report -b`), the check converts them to
bytes. Lines with empty mountpoint and device (`::data:...`), as written by older agent
scripts for the same section, are understood as well.

| Case | Default state |
| --- | --- |
| Used space in percent of the hard limit | WARN at 80%, CRIT at 90% |
| Hard limit (blocks or inodes) reached | CRIT |
| Soft limit (blocks or inodes) exceeded | WARN |
| Used inodes in percent of the inode limit (if set) | WARN at 80%, CRIT at 90% |
| Growth per time range, time left until full | no levels, shown in the details |

Projects without any limit (for example project `#0`) are not discovered. If the same
project name exists on more than one filesystem, the mount point is added to the item.

Metrics are the same as for the filesystem check (`fs_used`, `fs_free`, `fs_size`,
`fs_used_percent`, `inodes_used`, `fs_growth`, `fs_trend`, `trend_hoursleft`), so the
built-in graphs and the perfometer apply.

## Setup

1. Install the MKP on the Checkmk site.
2. Agent bakery: create the rule **XFS project quotas (Linux)** (default: run
   synchronously), bake and deploy the agent. Without the bakery copy `xfs_quota` to
   `/usr/lib/check_mk_agent/plugins/` and make it executable.
3. Run a service discovery on the host.
4. Optional: rule **XFS project quotas** (Storage) for:
   * levels on used or free space, in percent or absolute size
   * magic factor and reference size for percentage levels
   * the limit used as 100%: hard (default) or soft limit
   * states for an exceeded soft limit and a reached hard limit
   * levels for used inodes
   * trend range and levels on growth (bytes or percent) and time left until full

If an older check for the section `xfs_quota` is installed on the site (for example a
ported local check), remove it first, otherwise both plug-ins collide.

## Test data

| File | Content |
| --- | --- |
| `testdata/srv01_agent.txt` | WARN levels, hard limit reached, soft limit exceeded, inode limit |
| `testdata/srv02_legacy_format.txt` | output of an older agent script without mount point |
| `testdata/srv03_loop_xfs.txt` | real output of the plug-in on an XFS loop device with grace period running |
