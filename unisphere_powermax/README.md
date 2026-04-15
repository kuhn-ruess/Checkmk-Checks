# Unisphere PowerMax

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0p2-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p7-blue)
<!-- compatibility-badges:end -->

Special agent for Dell EMC Unisphere for PowerMax. Queries the Unisphere REST API at `https://<host>:<port>/univmax/restapi` and emits multiple Checkmk sections covering Storage Resource Pools, directors, port groups, masking views, volumes/ports, array performance, alert summaries, health scores and health checks.

## How it works

The special agent `agent_unisphere_powermax` authenticates with HTTP basic auth against the Unisphere REST API (default API version 100) and iterates over all Symmetrix systems returned by `/sloprovisioning/symmetrix`. By default it only queries systems flagged as `local`; remote Symmetrix systems can be enabled via a rule option. Results are printed as pipe-separated key/JSON lines under several section headers, with a 4-thread worker pool for masking-view detail queries and an on-disk cache under `$OMD_ROOT/tmp` for expensive masking view calls.

| Section | Data source / API |
| --- | --- |
| `unisphere_powermax_srp` | `/<v>/sloprovisioning/symmetrix/<id>/srp/<srp>` |
| `unisphere_powermax_director` | `/<v>/system/symmetrix/<id>/director/<dir>` |
| `unisphere_powermax_health_score` | `/<v>/system/symmetrix/<id>/health` |
| `unisphere_powermax_health_check` | `/<v>/system/symmetrix/<id>/health/health_check/<id>` |
| `unisphere_powermax_array_performance` | POST `/performance/Array/metrics` (Maximum + Average, 5 min window) |
| `unisphere_powermax_port_group` | `/<v>/sloprovisioning/symmetrix/<id>/portgroup` + port status |
| `unisphere_powermax_alerts` | `/<v>/system/alert_summary` |
| `unisphere_powermax_volume`, `unisphere_powermax_port` | masking view walk (cached) |

Each data source can be disabled individually through the WATO rule.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/unisphere_powermax/libexec/agent_unisphere_powermax` | Special agent (Python, uses `requests`). |
| `src/unisphere_powermax/server_side_calls/unisphere_powermax.py` | Builds the agent command line from rule parameters. |
| `src/unisphere_powermax/rulesets/rulesets.py` | Special-agent rule plus check-parameter rules for SRP / WP cache / health score / masking view / port group. |
| `src/unisphere_powermax/agent_based/unisphere_powermax_srp.py` | SRP effective/physical usage, data reduction ratio. |
| `src/unisphere_powermax/agent_based/unisphere_powermax_director.py` | Director status checks. |
| `src/unisphere_powermax/agent_based/unisphere_powermax_health_score.py` | Per-metric health score (lower levels). |
| `src/unisphere_powermax/agent_based/unisphere_powermax_health_check.py` | Symmetrix health check results. |
| `src/unisphere_powermax/agent_based/unisphere_powermax_array_performance.py` | Array performance + WP cache levels (Average / Maximum). |
| `src/unisphere_powermax/agent_based/unisphere_powermax_port_group.py` | Port-group / port state. |
| `src/unisphere_powermax/agent_based/unisphere_powermax_masking_view.py` | Masking view volume and port summaries. |
| `src/unisphere_powermax/agent_based/unisphere_powermax_alert.py` | Alert summaries (server + Symmetrix). |
| `src/unisphere_powermax/agent_based/utils.py` | Shared section parser. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a monitoring user on the Unisphere appliance with read access to the REST API.
3. Add the Unisphere host in Checkmk and configure the special agent rule (see below).

## Configuration

WATO rule: *Setup > Agents > Other integrations > Unisphere Powermax* (topic *Storage*).

| Parameter | Type | Meaning |
| --- | --- | --- |
| `username` | String (required) | Unisphere REST API user. |
| `password` | Password (required) | API password. |
| `port` | Integer (default 8443) | HTTPS port of Unisphere. |
| `api_version` | Integer (default 100) | REST API version prefix. |
| `use_ip` | Bool | Use the host's primary IP instead of its name for the HTTPS request. |
| `cache_time` | Integer (minutes, default 30) | Cache lifetime for masking view data. |
| `no_cert_check` | Bool | Disable SSL certificate verification. |
| `enable_remote_sym_checks` | Bool | Also query remote (non-local) Symmetrix systems. |
| `disable_get_srp_info` / `..._director_info` / `..._health_score_info` / `..._health_check_info` / `..._array_performance_info` / `..._port_group_info` / `..._alert_info` / `..._masking_view_info` | Bool | Disable individual data sources. |

A `_migrate` function silently upgrades older rule keys (`cache-time`, `useIP`, camelCase `disablegetXInfo`) to the new snake_case names.

Check parameter rules (topic *Storage*):

- *PowerMax SRP Effective usage* — upper % levels, default 80 / 90.
- *PowerMax SRP physical usage* — upper % levels, default 80 / 90.
- *PowerMax SRP Data Reduction Ratio* — lower levels on ratio, default 3.0 / 2.0.
- *PowerMax WP Cache usage* — upper % levels on Average and Maximum, default 80 / 90.
- *PowerMax Health Score* — lower % levels, default 90 / 80.
- *PowerMax Masking View Port Summary* — upper % levels.
- *PowerMax Masking View Volume Summary* — upper % levels.
- *PowerMax Port Group state* — upper % levels.

## Known limitations

- The agent uses a `--randomFailures` debug flag that can randomly flip port/volume status in the agent output — do not enable in production.
- The masking view section is refreshed only every `cache_time` minutes; shorter check intervals will see stale data.
- HTTP basic auth only; no OAuth / token support.
