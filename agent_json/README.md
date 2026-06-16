# Agent JSON

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-2.5-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p9-blue)
<!-- compatibility-badges:end -->

Special agent that queries one or more HTTP(S) endpoints and converts the returned JSON into Checkmk local checks. Useful for exposing arbitrary application health checks through REST endpoints without writing a dedicated plugin. Each endpoint has its own credentials and selectable HTTP method (POST by default, GET for endpoints that serve the JSON on GET).

## How it works

The agent script (`libexec/agent_json`) performs an HTTP request (`POST` by default, `GET` selectable per endpoint) to each configured URL, optionally using HTTP Basic Auth, and expects a JSON document of the form:

```text
{
  "checks": [
    {"name": "My Check", "status": "OK", "data": {"info1": "value", "info2": "more info"}},
    {"name": "Disks", "status": "WARN", "summary": "2 disks degraded",
     "data": {"sda": "ok", "sdb": "degraded"}},
    ...
  ]
}
```

Each entry is emitted as one line under the `<<<local>>>` section. The checks from all configured endpoints are merged into a single `<<<local>>>` section.

- **Status mapping:** the `status` string is mapped (case-insensitively) to a Checkmk state — `OK`/`UP` → `0`, `WARN`/`WARNING` → `1`, `CRIT`/`CRITICAL`/`DOWN` → `2`, `UNKN`/`UNKNOWN` → `3`. An unrecognised status becomes `3` (UNKNOWN).
- **Summary & details:** without a `summary` key the `data` dictionary is flattened into the summary line as comma-separated `key: value` pairs (legacy behaviour). If a `summary` key is present, its value is shown as the service summary and the `data` fields are rendered below it as multi-line details (one `key: value` per line).
- **Duplicate names:** when the same `name` appears more than once, repeated services are automatically numbered (`My Check`, `My Check 2`, …) so none get lost. Numbering spans all endpoints.
- **Failed endpoints:** if an endpoint returns something that is not parseable JSON, it is reported as a single `UNKNOWN` service (`JSON agent <url>`) including the HTTP status and a snippet of the body, so the failure stays visible instead of dropping out silently.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agent_json/libexec/agent_json` | Python special agent called by the Checkmk server. |
| `src/agent_json/server_side_calls/agent_json.py` | Builds the command line as `(api_url, user, password, method)` groups, one per endpoint. |
| `src/agent_json/rulesets/agent_json.py` | WATO form: a list of endpoints, each with URL, HTTP method, username and password. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create the host that should carry the local checks.
3. Configure the special agent rule (see below).

## Configuration

Rule: **Setup → Agents → Other integrations → Agent JSON**

Add one or more **endpoints**. Each endpoint has:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `api_url` | String (required) | Full URL the agent queries. |
| `method` | Choice (optional) | HTTP method: `POST` (default) or `GET`. |
| `username` | String (optional) | HTTP Basic Auth user. |
| `password` | Password (optional) | HTTP Basic Auth password. |

Rules saved with the previous single-URL format are migrated automatically into a one-entry endpoint list, so existing configuration keeps working without changes.
