# Bacula / Bareos Jobs Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.2.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.2.0p9-blue)
<!-- compatibility-badges:end -->

Monitors Bacula / Bareos backup jobs by querying the catalog database directly on the Director host. One Checkmk service per job name reports the most recent job state and the age of the last backup, with configurable allow / deny state lists and age thresholds.

## How it works

1. The Linux agent plugin [`bacula_jobs`](src/agents/plugins/bacula_jobs) reads `bacula.cfg` from `/etc/check_mk` (or uses defaults: MySQL backend, database `bacula`, user `bacula`, host `localhost`).
2. Depending on `backend_type` it queries MySQL/MariaDB or PostgreSQL:
   ```sql
   SELECT JobId, Name, JobStatus, EndTime FROM Job
   WHERE EndTime BETWEEN NOW() - 30 days AND NOW();
   ```
   For MySQL it uses `/root/.my.cnf` for credentials; for PostgreSQL it calls `psql` via `sudo -u <dbuser>`.
3. Output is emitted under `<<<bacula_jobs:sep(9)>>>`.
4. The check [`bacula_jobs`](src/checks/bacula_jobs) parses the rows, keeps only the newest entry per job name, and yields two results: current state (OK / WARN / CRIT based on the configured state lists) and age of the last backup (compared to `max_age` thresholds). One service `Job <name>` is created per job seen in the 30 day window.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/bacula_jobs` | Shell agent plugin run on the Bacula / Bareos Director host. |
| `src/agents/bakery/bacula` | Agent Bakery hook that deploys the plugin and writes `bacula.cfg`. |
| `src/checks/bacula_jobs` | Legacy check (`check_info`-style) with parser, discovery and check logic. |
| `src/checkman/bacula_jobs` | Check manual page. |
| `src/web/plugins/wato/bacula.py` | Legacy WATO rules: bakery deployment and per-job thresholds. |

## Installation

1. Install the MKP on the Checkmk site.
2. Deploy the agent plugin to the Director host:
   - **With Bakery:** configure *Agent Plugins -> Bacula Jobs (Linux)*, choose the backend type and DB credentials if they differ from the defaults, then bake the agent.
   - **Without Bakery:** copy `src/agents/plugins/bacula_jobs` to `/usr/lib/check_mk_agent/plugins/` and create `/etc/check_mk/bacula.cfg` with the variables `backend_type`, `dbhost`, `dbname`, `dbuser`.
3. Make sure the user running the Checkmk agent can read the catalog:
   - MySQL: `/root/.my.cnf` with matching credentials.
   - PostgreSQL: sudoers entry allowing `sudo -u <dbuser> psql`.
4. Run service discovery on the Director host.

## Configuration

Rule: **Setup -> Service monitoring rules -> Applications, Processes & Services -> Bacula Jobs**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `max_age` | `(warn, crit)` Age | Warning / critical thresholds on the age of the last backup (default 5 / 7 days). |
| `ok_states` | List of state codes | Bacula status codes reported as OK (default `T`, `R`). |
| `crit_states` | List of state codes | Bacula status codes reported as CRIT (default `E`, `f`). States not in either list become WARN. |

Known state codes: `T` terminated normally, `R` running, `E` terminated in error, `f` fatal error, `W` terminated with warning, `A` canceled, `C` created, `B` blocked, plus various waiting states.

## Services & metrics

- **Service:** `Job <name>` — one per distinct job name seen in the past 30 days.
- **State logic:** worst of state-lookup and age evaluation.
- **Metrics:** none.

## Known limitations

- Uses the legacy pre-2.3 check and WATO APIs (`check_info`, `register_rule`, `register_check_parameters`). Still loads on 2.3 / 2.4 as long as these APIs remain available.
- The plugin is hardcoded to look in `/etc/check_mk/bacula.cfg` (regardless of `MK_CONFDIR`).
- MySQL credentials are read from `/root/.my.cnf`, which means the agent user effectively needs root-equivalent access to that file.
- Jobs that have not run in the last 30 days disappear from discovery.
