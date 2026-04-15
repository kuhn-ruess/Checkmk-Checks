# A10 Loadbalancer Checks

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-1.6.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-1.6.0-blue)
<!-- compatibility-badges:end -->

SNMP-based monitoring for A10 AX loadbalancer appliances. Adds services for fans, power supplies and system temperature on top of the generic SNMP discovery.

## How it works

All three checks detect A10 devices via `sysObjectID` `.1.3.6.1.4.1.22610.1.3.22` and read from the A10-AX-MIB under `.1.3.6.1.4.1.22610.2.4.1.5`:

- Fans: `axFanName/Status/Speed` at `.9.1.{2,3,4}` — states `4..7` are OK, anything else CRIT.
- Power supplies: `axPowerSupplyName/Status` at `.12.1.{2,3}` — `on` is OK, `absent` CRIT, `off`/`unknown` WARN. Only supplies currently reporting `on` are discovered.
- Temperature: `axSyshwPhySystemTemp` at `.1` — delegates to the built-in `check_temperature` helper, so WARN/CRIT can be configured via the temperature ruleset.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/checks/a10_loadbalancer_fan` | Fan SNMP check (legacy `check_info` API). |
| `src/checks/a10_loadbalancer_power` | Power supply SNMP check. |
| `src/checks/a10_loadbalancer_temp` | System temperature check using `check_temperature`. |

## Installation

1. Install the MKP on the Checkmk site.
2. Add the A10 device as an SNMP host and run service discovery. The three checks auto-detect via `sysObjectID`.

## Services & metrics

- `Fan <name>` — one per fan, reports state and RPM.
- `Power Supply <name>` — one per power supply reporting `on` at discovery time.
- `Temperature System` — one service, WARN/CRIT from the temperature ruleset.

## Known limitations

- Uses the pre-2.0 `check_info` API. Still loads on newer Checkmk versions as long as the legacy API is available; needs porting to `cmk.agent_based.v2` if it ever drops.
- Power supplies that are in state `absent` or `off` at discovery time are not created as services.
