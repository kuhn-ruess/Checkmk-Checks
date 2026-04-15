# Bachmann EMA Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0p1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p25-blue)
<!-- compatibility-badges:end -->

SNMP check for Bachmann BlueNet EMA (Environmental Monitoring Adapter) GPIO ports. Discovers one service per enabled GPIO sensor and reports its mode, switch state and entity status.

## How it works

The plugin [`bachmann_ema.py`](src/bachmann_ema/agent_based/bachmann_ema.py) registers an SNMP section `bluenet_ema` that triggers on devices whose `sysDescr` starts with `Linux` and whose `sysLocation` starts with `Bachmann`. It walks `.1.3.6.1.4.1.31770.2.2.5.3.1` (BlueNet2 GPIO MIB) and collects, per GPIO pair:

- `5.1.4` / `5.1.5` — GPIO input IDs
- `8.1.4` / `8.1.5` — GPIO mode (`BlueNet2GPIOMode`)
- `10.1.4` / `10.1.5` — GPIO state
- `9.1.4` / `9.1.5` — GPIO switch

Services are discovered only where the mode is `enabled` (2) or `s0` (6). The check maps raw integer modes to human readable strings (`disabled`, `enabled`, `s0`, `undefined`), likewise for switch state (`on`, `off`, `switchable`, ...) and entity state (`ok`, `alarm`, `warning`, `armed`, `disarmed`, ...). An entity state of `39` (`armed`) is reported as CRIT; all other states are reported as OK.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/bachmann_ema/agent_based/bachmann_ema.py` | SNMP section parser, discovery and check. |

## Installation

1. Install the MKP on the Checkmk site.
2. Configure SNMP access (community or v3) for the EMA device and run service discovery. Services are named `EMA <input>/1` or `EMA <input>/2`.

## Services & metrics

- **Service:** `EMA %s` (GPIO pair)
- **State logic:** CRIT when the entity state is `armed` (39); otherwise OK.
- **Metrics:** none.

## Known limitations

- Only GPIOs whose mode is `enabled` or `s0` are discovered; disabled inputs are skipped silently.
- State mapping is hardcoded; only `armed` triggers CRIT, even though the MIB also exposes `alarm`, `errorHigh`, `lost`, `updateError` etc. These currently all surface as OK.
