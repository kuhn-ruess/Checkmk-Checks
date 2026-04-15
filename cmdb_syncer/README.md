# CMDB Syncer Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0p1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p8-blue)
<!-- compatibility-badges:end -->

Special agent that monitors jobs running inside [CMDB Syncer](https://github.com/Bastian-Kuhn/cmdbsyncer). It can report the status of named Syncer "services" (source jobs) and optionally the state of Syncer cron jobs, with one Checkmk service per configured job. Requires CMDB Syncer 3.9 or newer because an API username is now mandatory.

## How it works

The special agent `agent_cmdb_syncer` talks to the Syncer WebAPI at `<api_url>/api/v1/`:

- `syncer/services/<name>` — one request per configured service; output is emitted under `<<<cmdb_syncer_service:sep(0)>>>`, one JSON document per service id wrapped in `[[[<id>]]]` markers.
- `syncer/cron/` — fetched when `fetch_cron` is enabled; emitted under `<<<cmdb_syncer_cron:sep(0)>>>` as a single JSON list.

Authentication is sent via the `x-login-user: <username>:<password>` header. On HTTP 401 the agent synthesises an error record so the check turns CRIT with a clear message.

The check plugin `cmdb_syncer_service` creates `Service <id>` services and surfaces the API `message` field plus any `details`; it goes CRIT when `has_error` is true. The `cmdb_syncer_cron` plugin creates `Cron <name>` services and reports last message, running state, next planned run, and age of the last start; levels on last-start age are configurable.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/cmdb_syncer/libexec/agent_cmdb_syncer` | Special agent, queries the Syncer API. |
| `src/cmdb_syncer/agent_based/service.py` | `cmdb_syncer_service` and `cmdb_syncer_cron` section parsers and check plugins. |
| `src/cmdb_syncer/rulesets/agent.py` | Special agent ruleset (URL, credentials, services list, cron toggle). |
| `src/cmdb_syncer/rulesets/cron.py` | Check parameters for cron job max-age thresholds. |
| `src/cmdb_syncer/server_side_calls/cmdb_syncer.py` | Wires WATO params into the special agent command line. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a host in Checkmk for the Syncer API endpoint.
3. Configure the special agent rule (see below) and run service discovery. One service per configured source name is created, plus one `Cron <name>` per active cron when `fetch_cron` is enabled.

## Configuration

Rule: **Setup -> Agents -> Other integrations -> CMDB Syncer Monitoring**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `api_url` | String | Base URL including `http(s)://`. |
| `username` | String | Syncer API username (required since 3.9). |
| `password` | Password | API password for the user. |
| `timeout` | String (float) | Request timeout in seconds. |
| `services` | List of strings | Source names to monitor; one Checkmk service per entry. |
| `fetch_cron` | BooleanChoice | Also fetch and monitor cron jobs. |

Rule: **Parameters for discovered services -> CMDB Syncer Cron**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `max_time_since_last_start` | Levels (seconds) | Upper WARN/CRIT on the age of the last start timestamp. |

## Services & metrics

- **Services:** `Service <id>` (one per configured source), `Cron <name>` (one per cron when enabled).
- **State logic:** CRIT when the API reports `has_error`, when a cron has an error field, or when the last-start age exceeds the configured levels; WARN when a cron has never started.
