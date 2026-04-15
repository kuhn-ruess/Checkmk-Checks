# Arista Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-1.6.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.2.0p16-blue)
<!-- compatibility-badges:end -->

SNMP-based checks for Arista Networks devices using the generic entity sensor MIB. Adds services for temperature, fans and voltage derived from `entPhysicalDescr` combined with `entPhySensorValue/OperStatus/Units`.

## How it works

Detection is via `sysDescr` starting with `Arista Networks`. The parser joins four tables:

- `.1.3.6.1.2.1.47.1.1.1.1.2` — entity descriptions
- `.1.3.6.1.2.1.99.1.1.1.4` — sensor values
- `.1.3.6.1.2.1.99.1.1.1.5` — sensor status (`1` = OK, `2` = warning)
- `.1.3.6.1.2.1.99.1.1.1.6` — sensor units (`Celsius`, `RPM`, `Volts`, ...)

Items are discovered by unit:

- `arista` — unit `Celsius`, excluding descriptions starting with `PhyAlaska`. Values are divided by 10 and handed to `check_temperature`. Service `Temperature <name>`.
- `arista.fan` — unit `RPM`. Service `Fan <name>`, default lower levels 2000 / 1000 RPM, upper 9000 / 9500 RPM, using `check_fan`. The `Fan` prefix is stripped from the item name.
- `arista.voltage` — unit `Volts`. Service `Voltage <name>`, default lower levels 50 / 50 V.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/checks/arista` | Combined section + temperature, fan and voltage checks (legacy `check_info` API). |

## Installation

1. Install the MKP on the Checkmk site.
2. Add the Arista device as an SNMP host and run service discovery.

## Services & metrics

- `Temperature <name>` — WARN/CRIT from the temperature ruleset, with sensor status folded in.
- `Fan <name>` — RPM via `check_fan` with the lower/upper defaults shown above.
- `Voltage <name>` — voltage in volts with lower WARN/CRIT levels.

## Known limitations

- Uses the pre-2.0 `check_info` API with `temperature.include` and `fan.include`. Will keep working as long as Checkmk still ships the legacy API and include files.
- Entity descriptions starting with `PhyAlaska` are skipped for the temperature discovery to avoid spurious sensors.
