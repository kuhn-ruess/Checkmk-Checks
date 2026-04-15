# HP Proliant Status

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-1.6.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-1.6.0-blue)
<!-- compatibility-badges:end -->

Legacy 1.6-era SNMP check that reports the overall hardware condition of HP Proliant servers as a single `HW Status` service.

## How it works

The check reads `cpqHeMibCondition` from `.1.3.6.1.4.1.232.6.1.3` and maps the raw value to a Checkmk state:

| Value | Label | State |
| --- | --- | --- |
| `1` | other | UNKNOWN |
| `2` | ok | OK |
| `3` | degraded | CRIT |
| `4` | failed | CRIT |

Detection matches devices whose sysObjectID (`.1.3.6.1.4.1.232.2.2.4.2.0`) contains `proliant`.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/checks/hp_proliant_status` | Legacy 1.6 check definition (registers via `check_info`). |

## Installation

1. Install the MKP on a Checkmk 1.6 site.
2. Configure SNMP access to the server.
3. Run service discovery — a single `HW Status` service is created.

## Known limitations

- Uses the legacy 1.6 `check_info` API. For modern 2.x environments see the `hp` plugin in this repository, which provides an updated `General Status` check on top of `cmk.agent_based.v2`.
- `degraded` is mapped to CRIT (not WARN) as in the original module.
