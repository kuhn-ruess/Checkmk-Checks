# Pure checks

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p30-blue)
<!-- compatibility-badges:end -->

Special agent for Pure Storage FlashArray. Queries the FlashArray REST API
using the `purestorage` Python client and emits multiple Checkmk sections
covering alerts, array metadata, hardware components, drives, volumes,
volume performance, reduction details and TLS certificates.

## How it works

1. The special agent [`agent_pure`](src/pure/libexec/agent_pure) is
   invoked by the Checkmk site with the array IP and an API token. It
   opens a `purestorage.FlashArray` session and walks the following
   endpoints:
   - `list_messages(open=True)` -> `<<<pure_fa_errors>>>`: counts of
     critical / warning / info alerts.
   - `list_hardware()` -> `<<<pure_hardware>>>`: name, status, serial,
     speed, temperature, voltage, slot for each component (non-drive).
     Drives are filtered out here; a cache keeps the serial numbers for
     use in the drives section.
   - `list_drives()` -> `<<<pure_drives>>>`: drive name, status, serial,
     type, capacity. `unused` drives are skipped.
   - `get()` -> `<<<pure_array>>>`: array name, version, revision, id.
   - `list_volumes(space=True)` -> `<<<df>>>`: classic Checkmk filesystem
     section for each volume with size, used, free (in KB).
   - `list_volumes(action='monitor')` -> `<<<pure_arrayperformance>>>`:
     per-volume reads/writes, bandwidth, latency.
   - `list_volumes(space=True)` -> `<<<pure_arraydetails>>>`: data
     reduction, total reduction, shared / thin / snapshot / volume /
     size figures.
   - `list_certificates()` -> `<<<pure_arraycertificates>>>`: certificate
     name, common name, status, validity window and organisation info.
2. Check plugins under `src/pure/agent_based/` parse these sections and
   produce services for alerts, array inventory, array details, array
   performance, devices, hardware (fan / PSU / network / temp split out
   into separate modules), volumes (via the built-in `df` plugin) and
   certificates.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/pure/libexec/agent_pure` | Special agent talking to the FlashArray REST API via `purestorage`. |
| `src/pure/server_side_calls/pure.py` | Server-side call wiring: passes `-i <ip> -t <token>` to the agent. |
| `src/pure/rulesets/special_agent.py` | WATO special-agent ruleset `pure` with the API token field. |
| `src/pure/agent_based/alerts.py` | Section + check `pure_fa_errors` (alert counters). |
| `src/pure/agent_based/array.py` | Array inventory / summary check. |
| `src/pure/agent_based/arraydetails.py` | Data reduction / space details per volume. |
| `src/pure/agent_based/arrayperformance.py` | Per-volume performance metrics. |
| `src/pure/agent_based/arraycertificates.py` | Management certificate expiry check. |
| `src/pure/agent_based/devices.py` | Drives check. |
| `src/pure/agent_based/hardware.py` | Generic hardware components check. |
| `src/pure/agent_based/hardware_fan.py` | Fan components. |
| `src/pure/agent_based/hardware_psu.py` | Power supplies. |
| `src/pure/agent_based/hardware_nw.py` | Network components. |
| `src/pure/agent_based/hardware_temp.py` | Temperature sensors. |
| `src/pure/agent_based/utils/pure.py` | Shared parsing helpers. |
| `src/pure/graphing/arraydetails.py` | Metric / graph definitions for array details. |

## Installation

1. Install the `purestorage` Python package into the Checkmk site:
   `pip3 install --no-deps purestorage`
2. On the FlashArray, create an API token for a dedicated user via the UI
   (Settings -> API Client) or on the CLI: `pureadmin create --api-token`.
3. Install the MKP on the Checkmk site.
4. Add the FlashArray as a host. In the Checkmk configuration, create a
   host rule under *Setup -> Agents -> Other integrations -> Pure via
   WebAPI* and store the API token there.

## Configuration

Rule: **Setup -> Agents -> Other integrations -> Pure via WebAPI**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `token` | `Password` (required, non-empty) | FlashArray API token passed to `agent_pure` via `-t`. |

The host IP address is taken from `HostConfig.primary_ip_config` and
passed as `-i`.

## Services & metrics

Depending on the discovered sections, the following service groups are
created:

- Pure Alerts (critical / warning / info counts from the alert feed).
- Pure Array (name, version, revision, id).
- Pure Array Details / Performance per volume.
- Pure Drives / Hardware / Fans / PSUs / Network / Temperature
  (one service per physical component, CRIT when state is not healthy /
  ok).
- Volumes rendered as classic `df` filesystem services.
- Pure Array Certificates (one service per management certificate, with
  validity window).

## Known limitations

- Requires `purestorage` to be manually installed in the site - it is not
  shipped with the MKP.
- The agent prints plain error messages and exits on connection or API
  errors; nothing is retried.
- Hardware filtering is done by name prefix (`CH`, `SH`) and excludes
  entries containing `PWR` - non-standard hardware labels may be missed.
