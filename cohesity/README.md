# Cohesity checks

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p36-blue)
<!-- compatibility-badges:end -->

Special agent based monitoring for a Cohesity cluster. It queries the Iris REST API on the cluster VIP and produces services for cluster-wide alerts, per-node service health, storage and metadata usage, and counts of unprotected objects.

## How it works

The special agent `agent_cohesity` authenticates against `https://<vip>/irisservices/api/v1/public/accessTokens` and then calls:

- `/nexus/cluster/status` -> `<<<cohesity_node_status>>>` — one line per node reporting `ok` and `failed` service names.
- `/public/stats/storage` -> `<<<cohesity_storage_usage>>>` — `localUsageBytes`, `totalCapacityBytes`, etc.
- `/public/cluster` -> `<<<cohesity_metadata_usage>>>` — numeric fields including `usedMetadataSpacePct` and `availableMetadataSpace`.
- `/public/stats/alerts?startTimeUsecs=...&endTimeUsecs=...` (last 24h) -> `<<<cohesity_alerts>>>` — counts per severity.
- `/public/stats/protectionSummary` -> `<<<cohesity_unprotected>>>` — `numObjectsUnprotected`, `protectedSizeBytes`, etc.

Check plugins in `agent_based/` parse each section and create one service per result (nodes are keyed by hostname).

## Package contents

| Path | Purpose |
| --- | --- |
| `src/cohesity/libexec/agent_cohesity` | Special agent (REST client). |
| `src/cohesity/agent_based/cohesity_alerts.py` | `Alert Status` service from `/public/stats/alerts`. |
| `src/cohesity/agent_based/cohesity_node_status.py` | `Node Status <host>` per cluster node. |
| `src/cohesity/agent_based/cohesity_storage.py` | `Storage Status` with absolute and percent levels. |
| `src/cohesity/agent_based/cohesity_metadata.py` | `Metadata Status` with percent levels. |
| `src/cohesity/agent_based/cohesity_unprotected.py` | `Unproteced Status` (sic) for unprotected object count. |
| `src/cohesity/rulesets/cohesity_agent.py` | Special agent rule (user, password, domain, verify cert). |
| `src/cohesity/rulesets/cohesity_storage.py` | Check parameters for storage usage (absolute + percent). |
| `src/cohesity/rulesets/cohesity_metadata.py` | Check parameters for metadata usage (percent). |
| `src/cohesity/rulesets/cohesity_node_status.py` | Ignore-list for services in node status. |
| `src/cohesity/server_side_calls/cohesity_agent.py` | Command line generation for the special agent. |
| `src/cohesity/graphing/metrics.py` | Metric definitions. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a Checkmk host for the cluster VIP.
3. Configure the special agent rule and run service discovery.

## Configuration

Rule: **Setup -> Agents -> Other integrations -> Cohesity via WebAPI**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `user` | String | API username. |
| `password` | Password | Password for the user. |
| `domain` | String | Auth domain, default `LOCAL`. |
| `verify_cert` | BooleanChoice | Verify the cluster TLS certificate. |

Additional check parameter rules:

- **Cohesity storage** — absolute and percentage WARN/CRIT on used storage.
- **Cohesity metadata** — percentage WARN/CRIT on metadata usage.
- **Cohesity node status ignored services** — list of service names to exclude from the `ok` / `failed` summary.

## Services & metrics

- **Services:** `Alert Status`, `Node Status <host>`, `Storage Status`, `Metadata Status`, `Unproteced Status`.
- **Metrics:** `used_storage`, `percent_used`, `used_metadata_space_pct`, `avail_metadata_space`, `unprotected_objects`.

## Known limitations

- The unprotected service is spelled `Unproteced Status` in the source and kept that way for compatibility.
- Alerts are fetched for a fixed 24 hour window.
- `verify=False` is hardcoded in the REST client regardless of the `verify_cert` rule option.
