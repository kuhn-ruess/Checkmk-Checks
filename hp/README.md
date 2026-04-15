# HP Proliant General Status

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p5-blue)
<!-- compatibility-badges:end -->

SNMP monitoring for the overall health of HP Proliant servers. A single `General Status` service per host reports the mapped cpqHeMibCondition together with firmware version and serial number.

## How it works

The section is fetched via SNMP from the `.1.3.6.1.4.1.232` enterprise subtree:

- `.11.1.3.0` — cpqHeMibCondition (overall status)
- `.11.2.14.1.1.5.0` — firmware version
- `.2.2.2.1.0` — serial number

Detection matches hosts whose sysObjectID contains `8072.3.2.10` or `232.9.4.10`, or Windows SNMP agents (`.1.3.6.1.4.1.311.1.1.3.1.2`) that also expose `.1.3.6.1.4.1.232.11.1.3.0`. Status values are mapped as:

| Value | State | Label |
| --- | --- | --- |
| `0` | OK | OK |
| `1` | UNKNOWN | unknown |
| `2` | OK | OK |
| `3` | WARN | degraded |
| `4` | CRIT | failed |

Compared to the previous revision the mapping adds `0` as a valid OK state.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/cmk_addons_plugins/hp/agent_based/proliant.py` | SNMP section parser and check plugin. |

## Installation

1. Install the MKP on the Checkmk site.
2. Configure SNMP access to the HP Proliant server (iLO / host agent).
3. Run service discovery — a single `General Status` service is created.

## Services & metrics

- **Service:** `General Status`
- **Summary:** `Status: <mapped>, Firmware: <version>, S/N: <serial>`
