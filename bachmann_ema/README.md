# Bachmann EMA Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0p1-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.3.0p25-blue)
<!-- compatibility-badges:end -->

SNMP checks for Bachmann BlueNet2 PDUs: the EMA (Environmental Monitoring Adapter) GPIO ports and the overall state of the attached GPIO sensors.

## How it works

The plugin [`bachmann_ema.py`](src/bachmann_ema/agent_based/bachmann_ema.py) registers an SNMP section `bluenet_ema` that triggers on devices whose `sysDescr` starts with `Linux` and whose `sysLocation` starts with `Bachmann`. It walks `.1.3.6.1.4.1.31770.2.2.5.3.1` (BlueNet2 GPIO MIB) and collects, per GPIO pair:

- `5.1.4` / `5.1.5` — GPIO input IDs
- `8.1.4` / `8.1.5` — GPIO mode (`BlueNet2GPIOMode`)
- `10.1.4` / `10.1.5` — GPIO state
- `9.1.4` / `9.1.5` — GPIO switch

Services are discovered only where the mode is `enabled` (2) or `s0` (6). The check maps raw integer modes to human readable strings (`disabled`, `enabled`, `s0`, `undefined`), likewise for switch state (`on`, `off`, `switchable`, ...) and entity state (`ok`, `alarm`, `warning`, `armed`, `disarmed`, ...). An entity state of `39` (`armed`) is reported as CRIT; all other states are reported as OK.

## GPIO sensor state

The plugin [`bachmann_gpio_sensor.py`](src/bachmann_ema/agent_based/bachmann_gpio_sensor.py) registers an SNMP section `bluenet_gpio_sensor` for devices whose `sysObjectID` is below the Bachmann enterprise OID `.1.3.6.1.4.1.31770`. While `bluenet_ema` looks at the individual contacts of a GPIO sensor, this check reports the state of the sensor module itself, so a lost or switched off sensor is noticed even when no contact is wired.

It joins two tables:

- `.1.3.6.1.4.1.31770.2.2.4.2.1` (device table) — `3` name (`Master`, `Slave-1`, ...) and `4` friendly name (the rack position / "Stellplatz")
- `.1.3.6.1.4.1.31770.2.2.5.2.1` (sensor table) — `4` name, `5` friendly name, `7` sensor type OID, `8` state

Sensors are recognised as GPIO by their type OID (`.1.3.6.1.4.1.31770.2.1.8.3` external, `.1.3.6.1.4.1.31770.2.1.8.16` internal), with a fallback on a name starting with `GPIO`. Internal and external sensors are separate services; the type is part of the item name and of the check output.

Each service carries the service label `device_friendly_name:<friendly name of the PDU>`, so the rack position is available for filtering, views and NagVis/Orbvis hover menus.

State mapping (BlueNet2 `EntityState`): `on`, `ok`, `expected` are OK; `off`, `lost`, `alarm`, `errorHigh/Low`, `updateError` and the child alarm states are CRIT; the warning states, `disabled` and `updateInProgress` are WARN; anything unmapped is UNKNOWN.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/bachmann_ema/agent_based/bachmann_ema.py` | SNMP section parser, discovery and check for the single GPIO contacts. |
| `src/bachmann_ema/agent_based/bachmann_gpio_sensor.py` | SNMP section parser, discovery and check for the overall GPIO sensor state. |

## Installation

1. Install the MKP on the Checkmk site.
2. Configure SNMP access (community or v3) for the EMA device and run service discovery. Services are named `EMA <input>/1` or `EMA <input>/2`.

## Services & metrics

- **Service:** `EMA %s` (GPIO pair)
- **State logic:** CRIT when the entity state is `armed` (39); otherwise OK.
- **Metrics:** none.
- **Service:** `GPIO Sensor %s` (item: `<device> <sensor>`, e.g. `Master GPIO S1`, `Slave-2 GPIO Internal`)
- **Service label:** `device_friendly_name:<friendly name of the PDU>`
- **State logic:** see the state mapping above.
- **Metrics:** none.

## Known limitations

- Only GPIOs whose mode is `enabled` or `s0` are discovered; disabled inputs are skipped silently.
- State mapping is hardcoded; only `armed` triggers CRIT, even though the MIB also exposes `alarm`, `errorHigh`, `lost`, `updateError` etc. These currently all surface as OK.
- `GPIO Sensor` has no ruleset either: the mapping from BlueNet2 state to monitoring state cannot be changed without editing the plugin.
