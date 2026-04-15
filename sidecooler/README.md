# Sidecooler checks

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p30-blue)
<!-- compatibility-badges:end -->

SNMP-based monitoring for Sidecooler rack cooling units via the vendor MIB under `.1.3.6.1.4.1.46984.17`. The package ships seven check plugins covering device status, active alerts, fans, power supplies, warm/cold temperature bands, cold-water supply/return, and the cooling valve.

## How it works

All sections use `SimpleSNMPSection` with a detection rule of `exists(".1.3.6.1.4.1.46984.17.*")`. The table below summarises what each plugin reads and produces.

| Plugin | OID base | Service | Key behaviour |
| --- | --- | --- | --- |
| `sidecooler_status` | `.1.3.6.1.4.1.46984.17.1` (1-5) | `Sidecooler status` | Reports device, vendor, SW version, type and operating hours; emits an `uptime` metric (hours*3600). |
| `sidecooler_alerts` | `.1.3.6.1.4.1.46984.17.1` (10-20) | `Sidecooler alerts` | CRIT when `numAlert > 0`, lists the active alert strings; metric `alerts`. |
| `sidecooler_fans` | `.1.3.6.1.4.1.46984.17.3` (20-74) | `Sidecooler fan <1-6>` | One service per fan with a non-zero status. Reports power setpoint, current power, current RPM (with optional upper/lower levels from the `hw_fans` ruleset) and fan status. Metric `fan`. |
| `sidecooler_supply` | `.1.3.6.1.4.1.46984.17.3` (122-123) | `Sidecooler Supply A` / `B` | CRIT on power supply failure. |
| `sidecooler_temp` | `.1.3.6.1.4.1.46984.17.3` (1-8) | `Sidecooler Temp warm side` / `cold side` | Four sensors each (mean/top/center/bottom), individually configurable upper levels. Metrics `temp_warm_*`, `temp_cold_*`. Default levels `(30, 35)`. |
| `sidecooler_coldwater` | `.1.3.6.1.4.1.46984.17.3` (10-11) | `Sidecooler coldwater` | Supply and return water temperatures with configurable upper levels. Metrics `coldwater_supply`, `coldwater_return`. |
| `sidecooler_valve` | `.1.3.6.1.4.1.46984.17.3` (75-76) | `Sidecooler valve` | Reports setpoint and current valve opening in percent. Metrics `valve_set`, `valve_current`. |

All temperature and water values come in tenths and are divided by 10 in the parse function.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/sidecooler/agent_based/status.py` | Device status / uptime check. |
| `src/sidecooler/agent_based/alerts.py` | Active alert enumeration. |
| `src/sidecooler/agent_based/fan.py` | Per-fan check (6 fans). |
| `src/sidecooler/agent_based/supply.py` | Power supply A/B state. |
| `src/sidecooler/agent_based/temp.py` | Warm/cold side temperatures. |
| `src/sidecooler/agent_based/coldwater.py` | Cold-water supply and return temperatures. |
| `src/sidecooler/agent_based/valve.py` | Valve set/current. |
| `src/sidecooler/rulesets/temp.py` | WATO rule for per-sensor temperature levels. |
| `src/sidecooler/rulesets/coldwater.py` | WATO rule for cold-water levels. |
| `src/sidecooler/graphing/metrics.py` | Metric definitions. |
| `src/sidecooler/graphing/graphs.py` | Graph definitions. |

## Installation

1. Install the MKP on the Checkmk site.
2. Add the Sidecooler as an SNMP host. Detection is based on the presence of the Sidecooler MIB subtree.
3. Run service discovery.

## Configuration

| Rule | Purpose |
| --- | --- |
| *Sidecooler temperature* | Per-sensor upper levels for the four warm/cold side sensors (mean/top/center/bottom). |
| *Sidecooler coldwater* | Upper levels on `water_supply` and `water_return`. |
| Existing *Hardware fans* rule (`hw_fans`) | Upper and/or lower RPM levels for the fan check. |

## Known limitations

- The fan plugin stores its `fans` dict as a class attribute (shared between instances); this is benign because parsing always rewrites all six slots, but worth knowing when extending the code.
- Discovery only creates a fan service when its status is non-zero at discovery time.
