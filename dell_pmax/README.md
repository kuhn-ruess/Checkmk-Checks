# DELL EMC PowerMax

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0-blue)
<!-- compatibility-badges:end -->

Special agent for Dell EMC PowerMax (VMAX) arrays. It talks to the Unisphere for PowerMax REST API and produces services for Unisphere version, JVM/CPU/memory stats of the Unisphere server, server- and array-level alerts, and storage resource pool usage. This is a modernised port of the `dellpmax-agent` plugin originally published on the Checkmk Exchange by Mario Schwab and Achim Geisler.

## How it works

The special agent `agent_dellpmax` authenticates via HTTP basic auth against `https://<address>:<port>/univmax/restapi/` (default port 8443) and emits sections with `sep(124)`:

- `version` -> `<<<dellpmax_systeminfo>>>` — Unisphere version string.
- `management/RuntimeUsage/read` -> `<<<dellpmax_systemstats>>>` — heap (max/used), cpu usage, memory total/used. Split into three services (`Heap`, `CPU`, `Memory`) reusing `cmk.plugins.lib.memory` and `cpu_util`.
- `92/vvol/symmetrix` + `92/vvol/symmetrix/<id>` — discovers the local array id.
- `92/system/alert_summary` -> `<<<dellpmax_server_alerts>>>` and `<<<dellpmax_symm_alerts>>>` — unacknowledged warning/critical/fatal counts.
- `92/sloprovisioning/symmetrix/<id>/srp/...` -> `<<<dellpmax_storage_pools>>>` — per-SRP subscribed, snapshot, usable and effective used capacities.

Each SRP produces three services (`Subscribed Capacity <srp>`, `Snapshot Capacity <srp>`, `Usable Capacity <srp>`) with hardcoded 80/90 WARN/CRIT thresholds on the percentage values.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/dell_pmax/libexec/agent_dellpmax` | Special agent (Unisphere REST client). |
| `src/dell_pmax/agent_based/dellpmax_info.py` | `Version Info` service. |
| `src/dell_pmax/agent_based/dellpmax_system_stats.py` | `Heap`, `CPU`, `Memory` services from Unisphere runtime usage. |
| `src/dell_pmax/agent_based/dellpmax_alerts_server.py` | `Server alerts` service. |
| `src/dell_pmax/agent_based/dellpmax_alerts_symm.py` | `Array alerts` and `Performance alerts` services. |
| `src/dell_pmax/agent_based/dellpmax_storage_pools.py` | `Subscribed Capacity`, `Snapshot Capacity`, `Usable Capacity` per SRP. |
| `src/dell_pmax/rulesets/agent_dellpmax.py` | Special agent rule (username, password). |
| `src/dell_pmax/server_side_calls/agent_pmax.py` | Command line generation. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a host for the Unisphere appliance and configure the special agent rule below.
3. The API user only needs read-only monitoring role.
4. Run service discovery.

## Configuration

Rule: **Setup -> Agents -> Other integrations -> Dell Powermax**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `username` | String | Unisphere user with monitoring role. |
| `password` | Password | Password for the user. |

## Services & metrics

- **Services:** `Version Info`, `Heap`, `CPU`, `Memory`, `Server alerts`, `Array alerts`, `Performance alerts`, `Subscribed Capacity <srp>`, `Snapshot Capacity <srp>`, `Usable Capacity <srp>`.
- **State logic:**
  - Alerts: OK at 0, WARN/CRIT when warning/critical/fatal counters are non-zero.
  - Subscribed/Usable capacity: WARN at 80%, CRIT at 90%.
  - Snapshot capacity: always OK.

## Known limitations

- TLS certificate verification is hardcoded to off in the special agent.
- The WARN/CRIT thresholds for storage pools are hardcoded in the check plugin and not exposed via WATO.
- `port` cannot be configured through the ruleset; the special agent defaults to 8443.
