# Frafos Callcenter Metric

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.0.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.0.0p20-blue)
<!-- compatibility-badges:end -->

SNMP monitoring for Frafos SBC (Session Border Controller) callcenter systems. Provides a global `Call Statistics` service with total and per-minute call counts and one `Call Agent <name>` service per configured call agent with current, per-minute and traffic metrics in both directions.

## How it works

Both sections detect the device via `sysObjectID contains .1.3.6.1.2.1.1.2.0 = .1.3.6.1.4.1.8072` (Net-SNMP) and walk the Frafos SBC MIB under `.1.3.6.1.4.1.39695.2`.

- [`frafos_calls.py`](src/base/plugins/agent_based/frafos_calls.py) fetches `fSBCCallStarts` (`.3.0`) and `fSBCCalls` (`.4.0`) and emits a single `Call Statistics` service. Calls-per-minute is derived from the monotonic counter via `get_rate`.
- [`frafos_callagents.py`](src/base/plugins/agent_based/frafos_callagents.py) walks `.1.3.6.1.4.1.39695.2.2.1` and creates one `Call Agent <fSBCCAName>` service per entry with realm, current calls to/from, call-starts rate, and bytes/second in both directions.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/base/plugins/agent_based/frafos_calls.py` | Global `Call Statistics` SNMP section and check. |
| `src/base/plugins/agent_based/frafos_callagents.py` | Per call agent section and check. |

## Installation

1. Install the MKP on the Checkmk site.
2. Add the Frafos SBC as an SNMP host.
3. Run service discovery.

## Services & metrics

- **`Call Statistics`** — metrics `calls_current`, `calls_minute`.
- **`Call Agent <name>`** — metrics `current_to`, `current_from`, `to_per_minute`, `from_per_minute`, `current_bytes_to`, `current_bytes_from`.

## Known limitations

- Source still imports from the legacy `.agent_based_api.v1` namespace and uses `register.check_plugin` / `register.snmp_section`. This compiles on Checkmk 2.0–2.2 but will need porting to `cmk.agent_based.v2` for newer releases.
- Both plugins use the very generic Net-SNMP `.1.3.6.1.4.1.8072` detection, which will match on many non-Frafos devices; consider tightening if you monitor mixed SNMP hosts.
