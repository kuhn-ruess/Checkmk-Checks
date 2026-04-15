# Tridium Station Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-1.2.8-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-1.5.0p9-blue)
<!-- compatibility-badges:end -->

SNMP monitoring for Tridium Niagara stations (enterprise OID `.1.3.6.1.4.1.4131.1`). Probes are exposed as a flat name/value table where the value can be either a numeric reading or a textual state, and this plugin supports both, plus a rule-based cross-probe state check and a fuel tank check.

## How it works

The check script walks several subtrees below `.1.3.6.1.4.1.4131.1.6` and registers one check variant per subtree index. For every probe the plugin yields a service with a sensor name (OID column 2) and current value (OID column 3):

- `tridium_<N>` for `N in 2,3,7,8,9,10,11,13,14,15,16,17,19,23,24,25,26,27,28` — each creates services named `TR<N>` with item = sensor name. Numeric values are evaluated against WARN/CRIT levels; string values are checked against allow / force / discovery-locked state lists.
- `tridium_special` — merges two trees under `.1.3.6.1.4.1.4131.1.6.21` and `.22` and creates services `TRS <sensor>` that can be driven by a simple cross-probe rule: "if field X has state Y, require state Z on this probe, else require state W".
- `tridium_fuel` — reads the gasoline tank consumption/level from `.1.3.6.1.4.1.4131.1.6.15.1.1.3` and reports `TR Fuel` with metrics `usage`, `last_cons`, `level` (starting from a hardcoded 6000 ltr tank).

## Package contents

| Path | Purpose |
| --- | --- |
| `src/checks/tridium_station` | Legacy check script registering all `tridium_*` variants and the fuel check. |
| `src/web/plugins/wato/tridium.py` | Legacy WATO rules for `tridium`, `tridium_special`, `tridium_fuel`. |

## Installation

1. Install the MKP on the Checkmk site.
2. Configure SNMP on the Tridium station and add it as an SNMP host in Checkmk. Detection fires when `sysObjectID` starts with `.1.3.6.1.4.1.4131.1`.
3. Run service discovery.

## Configuration

WATO topic *Environment sensors*:

| Rule | Key parameters |
| --- | --- |
| *Tridium Device* | `levels` (warn/crit for numeric values), `allowed_strings`, `use_discovery` (lock state to the value seen at discovery), `forced_strings` (force CRIT on specific values). |
| *Tridium Special* | `rule` with `if_field`, `if_field_state`, `if_state`, `else_state` for cross-probe evaluation, or a simple `states` allow list. |
| *Tridium Fuel* | Lower warn/crit levels on remaining litres. |

## Services & metrics

- `TR<N> <sensor>` — numeric metric `value`; string values return OK unless excluded.
- `TRS <sensor>` — metric `value` when numeric; state driven by cross-probe rule.
- `TR Fuel` — metrics `usage`, `last_cons`, `level`.

## Known limitations

- Uses the pre-2.0 `check_info` / `register_check_parameters` API; the package `version.min_required` is `1.2.8`. Running on current Checkmk requires the legacy API shim to still be available.
- The fuel check hardcodes the tank size at 6000 litres.
- Tridium exposes data in a non-standard MIB; service items come from free-form probe names and may change when sensors are renamed on the station.
