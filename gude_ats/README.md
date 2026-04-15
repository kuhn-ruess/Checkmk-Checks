# GUDE ATS Input Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p5-blue)
<!-- compatibility-badges:end -->

SNMP monitoring for GUDE Automatic Transfer Switch devices. One `Input Status` service per device reports which input feed (Primary or Secondary) is currently active and alerts when either feed goes missing or when the active feed has switched away from the one seen at discovery time.

## How it works

The section is fetched via SNMP from `.1.3.6.1.4.1.28507.41.1.5.11`:

- `.1.0` — Primary Power Available
- `.2.0` — Secondary Power Available
- `.4.0` — Current Channel (1 = Primary, 2 = Secondary)

Detection matches sysDescr containing `UTE ATS`. At discovery the active channel is frozen into the service parameters as `inital`. The check reports CRIT when the current channel differs from the stored initial channel, and also CRIT when either the Primary or Secondary input shows `0` (void / not redundant).

## Package contents

| Path | Purpose |
| --- | --- |
| `src/cmk_addons_plugins/gude_ats/agent_based/ats.py` | SNMP section parser and check plugin. |

## Installation

1. Install the MKP on the Checkmk site.
2. Configure SNMP access to the GUDE ATS device.
3. Run service discovery — a single `Input Status` service is created.

## Services & metrics

- **Service:** `Input Status`
- **State logic:** CRIT if the active channel differs from the one seen at discovery, or if any input is reported as void.
