# Agent JSON

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-2.5-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p9-blue)
<!-- compatibility-badges:end -->

Special agent that POSTs to an HTTP(S) endpoint and converts the returned JSON into Checkmk local checks. Useful for exposing arbitrary application health checks through a single REST endpoint without writing a dedicated plugin.

## How it works

The agent script (`libexec/agent_json`) performs an HTTP `POST` to the configured URL, optionally using HTTP Basic Auth, and expects a JSON document of the form:

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

Each entry is emitted as one line under the `<<<local>>>` section.

- **Status mapping:** the `status` string is mapped (case-insensitively) to a Checkmk state — `OK`/`UP` → `0`, `WARN`/`WARNING` → `1`, `CRIT`/`CRITICAL`/`DOWN` → `2`, `UNKN`/`UNKNOWN` → `3`. An unrecognised status becomes `3` (UNKNOWN).
- **Summary & details:** without a `summary` key the `data` dictionary is flattened into the summary line as comma-separated `key: value` pairs (legacy behaviour). If a `summary` key is present, its value is shown as the service summary and the `data` fields are rendered below it as multi-line details (one `key: value` per line).
- **Duplicate names:** when the same `name` appears more than once, repeated services are automatically numbered (`My Check`, `My Check 2`, …) so none get lost.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agent_json/libexec/agent_json` | Python special agent called by the Checkmk server. |
| `src/agent_json/server_side_calls/agent_json.py` | Builds the command line `(api_url, user, password)`. |
| `src/agent_json/rulesets/agent_json.py` | WATO form for URL, username and password. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create the host that should carry the local checks.
3. Configure the special agent rule (see below).

## Configuration

Rule: **Setup → Agents → Other integrations → Agent JSON**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `api_url` | String (required) | Full URL the agent POSTs to. |
| `username` | String (optional) | HTTP Basic Auth user. |
| `password` | Password (optional) | HTTP Basic Auth password. |
