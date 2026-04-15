# Mysql Galera Cluster Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0p1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p8-blue)
<!-- compatibility-badges:end -->

Adds three check plugins for MySQL/MariaDB Galera clusters on top of the
built-in Checkmk `mysql` agent section: cluster state, per-node state
and replication health. No extra agent-side plugin is required — the
stock `mk_mysql` output already contains all the `wsrep_*` variables
needed.

## How it works

The plugins reuse the existing `mysql` section parsed by Checkmk.
Discovery walks each MySQL instance in the section and emits services
whenever `wsrep_provider_name` contains `galera`. Thresholds and
expected states are supplied via three separate rulesets.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/mysql_galera_cluster/agent_based/galera_cluster.py` | Three `CheckPlugin`s: `mysql_galera_cluster_cluster_state`, `mysql_galera_cluster_node_state`, `mysql_galera_cluster_repl_health`. |
| `src/mysql_galera_cluster/rulesets/params.py` | WATO rulesets `galera_cluster_state`, `galera_node_state`, `galera_repl_health`. |

## Installation

1. Install the MKP on the Checkmk site.
2. Deploy the normal Checkmk MySQL agent plugin (`mk_mysql`) on the
   Galera nodes so that the `<<<mysql>>>` section is present.
3. Run service discovery.

## Configuration

Rules live under *Service monitoring rules -> Applications*:

| Ruleset | Title | Parameters |
| --- | --- | --- |
| `galera_cluster_state` | MySQL Galera Cluster State | `wsrep_cluster_size` (lower levels), `wsrep_cluster_status` (`Primary` / `Non_primary` / `Disconnected`) |
| `galera_node_state` | MySQL Galera Node State | `wsrep_ready`, `wsrep_connected`, `wsrep_local_state_comment` |
| `galera_repl_health` | MySQL Galera Replication Health | `wsrep_local_recv_queue_avg`, `wsrep_local_send_queue_avg`, `wsrep_flow_control_paused` |

## Services & metrics

- `MySQL Galera Cluster State <instance>` — cluster size, status,
  configuration ID and state UUID.
- `MySQL Galera Node State <instance>` — ready / connected flag and
  `wsrep_local_state_comment`.
- `MySQL Galera Replication Health <instance>` — recv/send queue
  average, min, max and current; flow control paused, flow control
  recv/sent rates, cert deps distance.
