# Rittal Blue e+ Cooling Unit Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-2.5-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p25-blue)
<!-- compatibility-badges:end -->

Monitors **Rittal Blue e+** cooling units that are connected to a Rittal
**CMC III Processing Unit** or **IoT Interface** and polled via SNMP
(enterprise OID `.1.3.6.1.4.1.2606.7`).

## Why a separate plugin

The cmciii check bundled with Checkmk classifies sensors with a fixed
`sensor_type()` table that does not recognise the Blue e+ variable naming
scheme (`Internal Temperature`, `Monitoring.Cooling.Status`,
`Monitoring.Compressor.Speed`, …). As a result Blue e+ units are **never
discovered** by the built-in check, even though all of their data is present
in the CMC III variable table.

This plugin reads the same variable table (`.1.3.6.1.4.1.2606.7.4.2.2.1`),
filters to sub-devices whose device-table type is `Blue e+`
(`.1.3.6.1.4.1.2606.7.4.1.2.1`) and creates dedicated services.

## Services

| Service | Item | Content |
|---|---|---|
| `Blue e+ <name>` | e.g. `Blue e Plus 1` | Aggregated health of all component status fields (Cooling, Air Circuits, Fans, Compressor, EEV, Filter, Door, Electronics, Condensate, System Messages, Error List, temperature alarms). Performance data: input power, cooling capacity, EER. |
| `Blue e+ Temperature <name> <sensor>` | e.g. `Blue e Plus 1 Internal` | Internal / Ambient / External temperature with the appliance thresholds (overridable) and perfdata. |
| `Blue e+ <name> <fan>` | e.g. `Blue e Plus 1 Compressor` | Internal fan, external fan and compressor speed in percent with component status. |

Sensors/components reporting status *not available* are not discovered.

## Status mapping

The IoT Interface firmware reports only the numeric status code
(`cmcIIIVarValueStr` is empty), so codes are mapped from the
`RITTAL-CMC-III-MIB` `cmcIIIMsgStatus` enumeration to text and to a Checkmk
state. Defaults: `OK`/`closed`/`standby`/`active`/`detected` → OK,
`warning`/`high warning`/`low warning`/`config changed` → WARN,
`error`/`alarm`/`high alarm`/`low alarm`/`no power`/`lost` → CRIT. Override
per service with the **Rittal Blue e+ unit health** ruleset.

## Rulesets

- **Rittal Blue e+ unit health** — override the state per status text.
- **Rittal Blue e+ temperature** — upper temperature levels (otherwise the
  appliance thresholds are used).
