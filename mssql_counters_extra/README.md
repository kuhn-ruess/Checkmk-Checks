# MSSQL extra counters

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p9-blue)
<!-- compatibility-badges:end -->

Additional check plugins that reuse the built-in Checkmk `mssql_counters`
agent section to expose extra Microsoft SQL Server performance counters
that are not covered by the stock checks. One service per MSSQL instance
is created for each of the five counter groups.

## How it works

The plugins consume the existing `mssql_counters` section (no extra
agent-side code) and look for specific counter object IDs such as
`<instance>:Access_Methods`, `<instance>:General_Statistics`,
`<instance>:Latches`, `<instance>:Buffer_Manager` and
`<instance>:Memory_Manager`. For counter-style values (e.g.
`full_scans/sec`, `logins/sec`, `lazy_writes/sec`) the raw counters are
turned into per-second rates via `get_rate()`.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/mssql_counters_extra/agent_based/mssql_counters_access_methods.py` | Full scans, index searches, index hit ratio. |
| `src/mssql_counters_extra/agent_based/mssql_counters_connections.py` | User connections, logins/sec, logouts/sec. |
| `src/mssql_counters_extra/agent_based/mssql_counters_latches.py` | Latch waits/sec, total and average latch wait time. |
| `src/mssql_counters_extra/agent_based/mssql_counters_memory.py` | Lazy writes/sec, page life expectancy, memory grants pending, memory usage vs. target. |
| `src/mssql_counters_extra/agent_based/mssql_counters_work_files_tables.py` | Workfiles/sec and worktables/sec. |
| `src/mssql_counters_extra/rulesets/*.py` | WATO rule specs for each of the above check plugins. |

## Installation

1. Install the MKP on the Checkmk site.
2. The stock Checkmk MSSQL agent plugin (`mssql.vbs` / `mssql.ps1`) must
   already be deployed on the monitored hosts so that the
   `mssql_counters` section is available.
3. Run service discovery on the MSSQL host.

## Configuration

Rules live under *Service monitoring rules -> Applications* with these
titles and ruleset names:

| Ruleset | Title | Parameters |
| --- | --- | --- |
| `mssql_counters_access_methods` | MSSQL index usage | `AccessFullScans`, `AccessIndexSearches`, `index_hit_ratio` |
| `mssql_counters_connections` | MSSQL user connections | `user_connections`, `LogInConnects`, `LogOutConnects` |
| `mssql_counters_latches` | MSSQL latches | `LatchWaits`, `LatchWaitTime`, `LatchAverage` |
| `mssql_counters_memory` | MSSQL memory usage | `LazyWrites`, `page_life_expectancy`, `MemoryGrantsPending`, `MemoryUsage` |
| `mssql_counters_work_files_tables` | MSSQL workfiles / worktables | `WorkFiles`, `WorkTables` |

All parameters use `SimpleLevels` with sensible defaults.

## Services & metrics

| Check plugin | Service name | Key metrics |
| --- | --- | --- |
| `mssql_counters_access_methods` | `MSSQL <instance> Access Index Usage` | `perf_AccessFullScans`, `perf_AccessIndexSearches`, `index_searches_per_full_scan`, `index_hitratio` |
| `mssql_counters_connections` | `MSSQL <instance> User Connections` | `user_connections`, `logins_per_sec`, `logouts_per_sec` |
| `mssql_counters_latches` | `MSSQL <instance> Latch Waits` | `latch_waits_per_sec`, `latch_wait_time`, `avg_latch_wait_time` |
| `mssql_counters_memory` | `MSSQL Memory <instance>` | `perf_LazyWrites`, `perf_page_life_expectancy`, `perf_MemoryGrantsPending`, `perf_MemoryUsage` |
| `mssql_counters_work_files_tables` | `MSSQL <instance> WorkFiles and WorkTables` | `perf_WorkFiles`, `perf_WorkTables` |
