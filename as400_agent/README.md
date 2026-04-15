# AS 400 Agent

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0p1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p8-blue)
<!-- compatibility-badges:end -->

Special agent for IBM AS/400 (IBM i) monitoring. Connects to the system via ODBC (pyodbc) and creates one Checkmk service per active job by querying `QSYS2.ACTIVE_JOB_INFO()`.

## How it works

The special agent script [`agent_as400_agent`](src/as400_agent/libexec/agent_as400_agent) opens an ODBC connection using the driver, system name, user ID and password passed from the special agent rule, runs `SELECT * FROM TABLE(QSYS2.ACTIVE_JOB_INFO())`, and prints each job as a sub-section under the `<<<as400_agent_jobs>>>` header. The agent based plugin [`jobs.py`](src/as400_agent/agent_based/jobs.py) discovers one `Job <JOB_NAME>` service per job and reports `JOB_TYPE`, `JOB_STATUS`, `JOB_END_REASON`, `JOB_DESCRIPTION` and `JOB_ACTIVE_TIME` as OK results.

### Example agent output

```text
<<<as400_agent_jobs>>>
[[[123456/USER/JOBNAME]]]
JOB_NAME 123456/USER/JOBNAME
JOB_STATUS ACTIVE
JOB_TYPE BCH
...
```

## Package contents

| Path | Purpose |
| --- | --- |
| `src/as400_agent/libexec/agent_as400_agent` | Special agent script (pyodbc client for AS/400). |
| `src/as400_agent/agent_based/jobs.py` | Section parser and check plugin for `as400_agent_jobs`. |
| `src/as400_agent/rulesets/ruleset.py` | WATO special agent rule (`cmk.rulesets.v1`). |
| `src/as400_agent/server_side_calls/agent_as400.py` | Command builder passing driver, system, uid, password. |

## Installation

1. Install the MKP on the Checkmk site.
2. On the Checkmk server, install `pyodbc` for the site user (`pip3 install pyodbc`) and set up the IBM i Access ODBC Driver so that the driver name configured in the rule (default `{IBM i Access ODBC Driver}`) resolves.
3. Create a host for the AS/400 system and configure the special agent rule *AS400 Agent*.

## Configuration

Rule: **Setup -> Agents -> Other integrations -> AS400 Agent**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `driver` | String | ODBC driver name, e.g. `{IBM i Access ODBC Driver}`. |
| `system` | String | Host / system name of the AS/400. |
| `uid` | String | Database user ID. |
| `password` | Password | Password for the database user. |

## Services & metrics

- **Service:** `Job <JOB_NAME>` (one per active job)
- Always reports `State.OK` with job metadata; no metrics, no thresholds.

## Known limitations

- Currently no thresholds or allow/deny lists on job state; `check_ruleset_name` is not wired up.
- Every active job becomes a service, so discovery on busy LPARs can produce a very large number of services.
