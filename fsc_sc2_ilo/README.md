# FSC SC2 ILO Disk Checks

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p18-blue)
<!-- compatibility-badges:end -->

Adds SNMP disk health monitoring for Fujitsu Siemens (FSC) ServerView SC2 iRMC / ILO hosts, complementing the existing built-in FSC checks. One `Disk <name>` service is created per physical disk reported by the SC2 MIB, with status decoded to Checkmk states.

## How it works

[`fsc_sc2_ilo_disks.py`](src/fsc_sc2_ilo/agent_based/fsc_sc2_ilo_disks.py) defines a `SimpleSNMPSection` under the Fujitsu enterprise OID tree:

```text
detect: sysObjectID startswith .1.3.6.1.4.1.231
base:   .1.3.6.1.4.1.231.2.49.1.5.2.1
oids:   .15 (health status), .24 (disk name)
```

Disks reporting status `2` (not-present) or `4` (disabled) are skipped during discovery. The check maps status numbers to Checkmk states:

| Status | Meaning | State |
| --- | --- | --- |
| 2 | not-present | CRIT |
| 3 | ok | OK |
| 4 | disabled | OK |
| 5 | error | CRIT |
| 6 | failed | CRIT |
| 7 | prefailure-predicted | WARN |
| 11 | hidden | OK |

Anything else is reported as UNKNOWN.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/fsc_sc2_ilo/agent_based/fsc_sc2_ilo_disks.py` | SNMP section and check plugin for `fsc_sc2_ilo_disks`. |

## Installation

1. Install the MKP on the Checkmk site.
2. Make sure the FSC host is monitored via SNMP so the Fujitsu MIB is reachable.
3. Run service discovery. A `Disk <name>` service appears for every present disk.

## Services

- `Disk <name>` — one per physical disk reported by the SC2 MIB.
