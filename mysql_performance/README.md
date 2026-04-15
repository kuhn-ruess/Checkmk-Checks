# Mysql Performance Checks

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.0.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.2.0-blue)
<!-- compatibility-badges:end -->

Adds a MySQL Thread Cache hit-rate subcheck on top of the built-in
Checkmk MySQL monitoring. No extra agent plugin is required — the stock
`mk_mysql` section is consumed directly.

## How it works

The check plugin reads `Threads_created` and `Connections` from the
`mysql` section and computes the Thread Cache hit rate as
`(Threads_created / Connections) * 100`. One service
`MySQL <instance> Thread Cache` is discovered per MySQL instance.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agent_based/mysql_performance.py` | Check plugin on the legacy `agent_based_api.v1` register API. |
| `src/web/plugins/wato/mysql.py` | WATO ruleset `mysql_tchitrate`. |

## Installation

1. Install the MKP.
2. Deploy `mk_mysql` on the MySQL hosts.
3. Run service discovery.

## Services & metrics

- **Service:** `MySQL <instance> Thread Cache`
- **Metric:** `percent` — thread-cache hit rate in %.
- **State logic:** WARN at >=80, CRIT at >=90 (currently hardcoded in
  the check function).

## Known limitations

- The check plugin still uses the pre-2.3 `agent_based_api.v1` register
  API (`from .agent_based_api.v1 import register`).
- The WATO file uses the legacy `register_check_parameters` API.
- WARN/CRIT levels are hardcoded to 80/90 in the check function; the
  ruleset value is not yet honoured (see `# TODO` in the source).
