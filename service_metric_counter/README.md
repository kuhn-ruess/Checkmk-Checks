# Count the Value of Service Perfdata Metrics

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0p1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p25-blue)
<!-- compatibility-badges:end -->

Special agent that sums a named performance-data metric across all Checkmk services matched by a Livestatus-style filter and exposes the total as its own Checkmk service. Example use case: add up the `users` metric of every matching `Users` service in a distributed setup and alert on a global upper level.

## How it works

1. For each configured entry the agent queries the central Checkmk REST API
   (`<path>/check_mk/api/1.0/domain-types/service/collections/all`) with a Livestatus query built from the `ls_pattern` string. Sub-patterns are separated by `;`, each sub-pattern uses `=` or `~` as operator (e.g. `description~Users;host_labels='env' 'prod'`).
2. The returned `performance_data` dict is summed over the configured metric name.
3. One line per entry is emitted under `<<<service_metric_counter:sep(58)>>>` in the form
   `<service_name>:<total>:<metric>:<label>`.
4. The `service_metric_counter` check creates a service `Service <service_name>` per entry, reports the sum as a metric and compares it against optional upper levels.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/service_metric_counter/libexec/agent_service_metric_counter` | Special agent that queries the REST API. |
| `src/service_metric_counter/server_side_calls/service_counter.py` | Server-side call wiring. |
| `src/service_metric_counter/rulesets/ruleset.py` | WATO rules for the special agent and the check parameters. |
| `src/service_metric_counter/agent_based/service.py` | Section parser and `service_metric_counter` check plugin. |

## Installation

1. Install the MKP on the Checkmk site.
2. Pick a monitoring host to carry the aggregated services and configure the special agent rule on it.
3. Run service discovery.

## Configuration

Rule: **Setup -> Agents -> Other integrations -> Service Metric counter**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `path` | String | Base URL of the Checkmk site, e.g. `https://server/site/`. Required because the agent may run on a remote site. |
| `timeout` | Time span | REST API request timeout (default 2.5s). |
| `service_filters` | List of entries | Each entry defines one aggregated service. |
| &nbsp;&nbsp;`service_name` | String | Item of the resulting service. |
| &nbsp;&nbsp;`ls_pattern` | String | Livestatus filter, e.g. `description~Users;host_labels='env' 'prod'`. |
| &nbsp;&nbsp;`metric` | String | Name of the performance metric to sum. |
| &nbsp;&nbsp;`metric_label` | String | Human-readable label shown in the service output. |

Rule: **Parameters for discovered services -> Service Metric Count**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `levels` | Upper levels (count) | Optional WARN/CRIT on the summed value. |

## Services & metrics

- **Service:** `Service <service_name>` — one per configured entry.
- **Metric:** name taken from the configured `metric` field. The value is the sum across all matched services.
