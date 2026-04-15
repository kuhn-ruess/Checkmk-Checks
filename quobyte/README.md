# Quobyte Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p9-blue)
<!-- compatibility-badges:end -->

Special agent for Quobyte storage clusters. Talks to the Quobyte JSON-RPC
WebAPI and emits piggyback output for each cluster host, covering
services, health manager, devices, volumes and quotas. Ships check
plugins, a WATO rule, graphing definitions and a server-side-calls
binding.

## How it works

The special agent [`agent_quobyte`](src/quobyte/libexec/agent_quobyte) is
invoked with API URL, username, password and timeout. It POSTs JSON-RPC
calls and emits the following sections:

- `<<<quobyte_services>>>` (piggybacked per service host): list of
  service types and their `is_available` flag from `getServices`.
- `<<<quobyte_healthmanager>>>`: full `health_manager_status` dict from
  `getHealthManagerStatus` (one `key value` line each).
- `<<<quobyte_devices>>>` (piggybacked per device host): device id,
  serial, label, used/total bytes, status, LED status, mount path and
  health for each entry from `getDeviceList`.
- `<<<quobyte_volumes>>>`: per-volume logical/disk/allocated bytes plus
  file and directory counts from `getVolumeList`.
- `<<<quobyte_quotas>>>`: per quota entry (`[[[<type> <consumer_type>
  <identifier>]]]`) with `limit`, `usage`, `limit_type` and `tenant_id`,
  resolving volume UUIDs to volume names.

Check plugins under `src/quobyte/agent_based/` consume these sections:

| File | Section |
| --- | --- |
| `devices.py` | `quobyte_devices` - one service per device, CRIT if not healthy. |
| `healthmanager.py` | `quobyte_healthmanager` - health manager status overview. |
| `quota.py` | `quobyte_quotas` - one service per quota, usage vs. limit. |
| `services.py` | `quobyte_services` - one service per Quobyte component on a host. |
| `volumes.py` | `quobyte_volumes` - one service per volume. |

Graph, metric and perfometer definitions live under `src/quobyte/graphing/`.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/quobyte/libexec/agent_quobyte` | Special agent (JSON-RPC client to the Quobyte WebAPI). |
| `src/quobyte/server_side_calls/quobyte.py` | Server-side-call wiring: passes `api_url username password timeout` as positional arguments. |
| `src/quobyte/rulesets/agent.py` | WATO special-agent ruleset `quobyte`. |
| `src/quobyte/rulesets/volumes.py` | WATO ruleset for volume check parameters. |
| `src/quobyte/agent_based/devices.py` | Devices check. |
| `src/quobyte/agent_based/healthmanager.py` | Health manager check. |
| `src/quobyte/agent_based/quota.py` | Quotas check. |
| `src/quobyte/agent_based/services.py` | Services check. |
| `src/quobyte/agent_based/volumes.py` | Volumes check. |
| `src/quobyte/graphing/graphs.py` | Graph definitions. |
| `src/quobyte/graphing/metrics.py` | Metric definitions. |
| `src/quobyte/graphing/perfometer.py` | Perfometer definitions. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a Checkmk host for the Quobyte cluster.
3. Configure the special agent via *Setup -> Agents -> Other integrations
   -> Quobyte via WebAPI*. Provide the API URL, a user with read access
   and the matching password; optionally override the timeout.
4. Run service discovery on the cluster host. Additional services will
   appear on piggyback hosts named after the Quobyte service/device
   hosts.

## Configuration

Rule: **Setup -> Agents -> Other integrations -> Quobyte via WebAPI**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `api_url` | `String` (required) | Full URL of the Quobyte JSON-RPC endpoint. |
| `username` | `String` (required) | API user. |
| `password` | `Password` (required) | API password. |
| `timeout` | `TimeSpan` (optional, default 2.5 s) | Request timeout. |

A separate ruleset is available for volume check parameters under the
normal *Parameters for discovered services* tree.

## Services & metrics

- Devices services (piggyback, one per device) with usage and health.
- Health manager overview service.
- One service per Quobyte component per host.
- One service per volume (with space and file/dir counters).
- One service per quota (usage vs. limit).

## Known limitations

- Credentials are passed as positional CLI arguments to the agent
  (`api_url username password timeout`); they therefore appear in the
  agent process arguments on the Checkmk server.
- The `timeout` default in the server-side call model is `"15.0"` as a
  string and only the ruleset default of 2.5 s takes effect; do not rely
  on the Python type annotation.
- Quota parsing assumes a single `current_usage` entry per quota - the
  source explicitly notes this may be wrong for multi-metric quotas.
