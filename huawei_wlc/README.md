# Huawei WLC Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-1.6.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-1.6.0-blue)
<!-- compatibility-badges:end -->

Legacy 1.6-era SNMP check for Huawei Wireless LAN Controllers. One service per access point reports the AP run state, management IP, up/down traffic, and the number of online users.

## How it works

The check walks `.1.3.6.1.4.1.2011.6.139.13.3.3.1` on devices whose sysObjectID equals `.1.3.6.1.4.1.2011.2.240.6` and reads:

- `.4` — `hwWlanApName`
- `.6` — `hwWlanApRunState`
- `.13` — `hwWlanApIpAddress`
- `.58` — `hwWlanApAirportUpTraffic`
- `.59` — `hwWlanApAirportDwTraffic`
- `.44` — `hwWlanApOnlineUserNum`

Run state is mapped via a static dictionary (`idle`, `autofind`, `typeNotMatch`, `fault`, `config`, `configFailed`, `download`, `normal`, `committing`, `commitFailed`, `standby`, `verMismatch`, `nameConflicted`, `invalid`). States `fault`, `configFailed`, `commitFailed`, `nameConflicted`, `invalid` map to CRIT; `verMismatch` and `standby` map to WARN.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/checks/huawei_wlc` | Legacy 1.6 check definition (registers via `check_info`). |

## Installation

1. Install the MKP on a Checkmk 1.6 site.
2. Configure SNMP access to the WLC.
3. Run service discovery — one `AP <name>` service per access point is created.

## Services & metrics

- **Service:** `AP <name>` — one per AP
- **Metric:** `users` (number of currently associated clients)
