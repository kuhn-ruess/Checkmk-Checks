# AudioCode Gateway

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p5-blue)
<!-- compatibility-badges:end -->

SNMP checks for AudioCodes SIP gateways and SBCs. Adds services for active alarms, SBC call and user statistics, SIP interface and IP group configuration, and Tel2IP / IP2Tel performance counters. Based on earlier work by Robert Sander.

## How it works

All sections detect the device via `sysObjectID` containing `.1.3.6.1.4.1.5003.8.1.1` and query the AudioCodes private MIB tree under `.1.3.6.1.4.1.5003`:

- `acgateway_alarms` — reads active alarms and history sequence numbers from `acAlarm` (`.11.1.1.1.1` / `.11.1.2.1.1`). Severity `major/critical` maps to CRIT, `warning/minor` to WARN. Service `SIP Alarms` also exposes `active_alarms` and `archived_alarms` metrics.
- `acgateway_calls` — SBC active calls, ASR, ACD and call rate from `acPMSIPSBC*` and `acPMSBC*`. Service `SBC Calls`.
- `acgateway_users` — SBC registered users and SIP transaction rates. Service `SBC Users`.
- `acgateway_sipperf` — Tel2IP and IP2Tel counters from `acPerfH323SIPGateway` (attempted / established / busy / no-answer / no-route / fail / fax / duration), reported as rates. Service `SIP Performance`.
- `acgateway_sipinterface` — joins SIP interface, system interface and ethernet device rows; service per interface named `<index> <name>`, discovered row status becomes part of the service parameters and deviations go CRIT.
- `acgateway_ipgroup` — IP group row status, type and description; service per `<index> <name>`.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/acgateway/agent_based/alarms.py` | Active and archived alarms section and check. |
| `src/acgateway/agent_based/calls.py` | SBC established calls, ASR, ACD. |
| `src/acgateway/agent_based/users.py` | SBC registered users and SIP transactions per second. |
| `src/acgateway/agent_based/sipperf.py` | Tel2IP / IP2Tel performance counters. |
| `src/acgateway/agent_based/sipinterface.py` | SIP interface + underlying system interface and ethernet device. |
| `src/acgateway/agent_based/ipgroup.py` | IP group status, type and description. |
| `src/acgateway/checkman/acgateway_ipgroup` | Check manual page. |
| `src/acgateway/checkman/acgateway_sipinterface` | Check manual page. |
| `src/acgateway/graphing/acgateway.py` | Metric definitions for the performance counters. |

## Installation

1. Install the MKP on the Checkmk site.
2. Add the AudioCodes gateway as an SNMP host and run service discovery.

## Services & metrics

| Service | Notes |
| --- | --- |
| `SIP Alarms` | State driven by active alarm severity. Metrics: `active_alarms`, `archived_alarms`. |
| `SBC Calls` | Metrics: `active_calls`, `calls_per_sec`, `average_success_ratio`, `average_call_duration`. |
| `SBC Users` | Metrics: `rx_trans`, `tx_trans`, `num_user`. |
| `SIP Performance` | Metrics: `tel2ip_*` and `ip2tel_*` counters (attempted, established, busy, no_answer, no_route, no_capability, failed, fax_attempted, fax_success, total_duration). |
| `SIP Interface <index> <name>` | Discovery saves row status; any later change goes CRIT. |
| `IP Group <index> <name>` | Discovery saves row status; any later change goes CRIT. |
