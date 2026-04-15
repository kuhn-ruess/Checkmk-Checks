# Check for MySQL status variables

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p8-blue)
<!-- compatibility-badges:end -->

Exposes a wide set of `SHOW GLOBAL STATUS` variables as individual
Checkmk services on top of the stock MySQL agent section. No additional
agent plugin is required; this plugin works as a subcheck for the
normal Checkmk MySQL monitoring.

## How it works

The check plugin consumes the built-in `mysql` section. It iterates
over every MySQL instance in the section and emits one service per
variable listed in its inventory table. Counter variables are
converted to per-second rates via `get_rate()`, gauges are reported
verbatim, and boolean variables (e.g. `Slave_running`, `Compression`)
are compared against a configured target state.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/mysql_status/agent_based/mysql_status.py` | `CheckPlugin` `mysql_status` with inventory table mapping each variable to `Counter` / `Gauge` / `Boolean`. |
| `src/mysql_status/rulesets/mysql_status.py` | WATO ruleset `mysql_status` (upper levels and target state). |
| `src/mysql_status/graphing/mysql_status.py` | Metric definitions. |
| `src/mysql_status/checkman/mysql_status` | Check manual page. |

## Installation

1. Install the MKP.
2. Deploy `mk_mysql` on the MySQL hosts.
3. Run service discovery — one service per supported status variable
   per instance.

## Configuration

Rule: *Service monitoring rules -> Applications -> Settings for MySQL
status check* (ruleset `mysql_status`, per item).

| Parameter | Type | Meaning |
| --- | --- | --- |
| `levels` | Upper `SimpleLevels[Integer]` | Upper WARN/CRIT on the rate (Counter) or current value (Gauge). |
| `target_state` | SingleChoice `on` / `off` | Expected value for Boolean variables (e.g. `Slave_running`). |

## Services & metrics

- **Service:** `MySQL Status <instance> <variable>`
- **Metric:** `mysql_status_<variable_lowercase>`
- **Monitored variables:** `Aborted_clients`, `Aborted_connects`,
  `Bytes_received`, `Bytes_sent`, `Compression`, `Connections`,
  `Created_tmp_disk_tables`, `Created_tmp_files`, `Created_tmp_tables`,
  `Innodb_buffer_pool_pages_free`, `Innodb_buffer_pool_read_requests`,
  `Innodb_buffer_pool_reads`, `Innodb_buffer_pool_write_requests`,
  `Innodb_log_waits`, `Innodb_os_log_written`, `Innodb_row_lock_time`,
  `Innodb_row_lock_waits`, `Key_blocks_unused`, `Key_read_requests`,
  `Key_reads`, `Key_write_requests`, `Key_writes`, `Open_tables`,
  `Open_files`, `Qcache_free_memory`, `Qcache_free_blocks`,
  `Qcache_hits`, `Qcache_inserts`, `Qcache_low_mem_prunes`,
  `Qcache_lowmem_prunes`, `Qcache_not_cached`, `Queries`, `Questions`,
  `Select_full_join`, `Select_range_check`,
  `Slave_retried_transactions`, `Slave_running`, `Slow_launch_threads`,
  `Slow_queries`, `Sort_merge_passes`, `Table_locks_waited`,
  `Threads_cached`.
