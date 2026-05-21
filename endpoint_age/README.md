# HTTP endpoint freshness monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.4.0-blue)
<!-- compatibility-badges:end -->

Generic check that verifies an HTTP endpoint is still being kept up to date by an upstream producer (a cron job, a CDN cache, a periodic export, ...). The accompanying special agent fetches each configured URL and derives an "age in seconds" from one of three sources, then applies WARN/CRIT thresholds to that age.

## How it works

The agent script `agent_endpoint_age` accepts one or more `--endpoint JSON` arguments. For every endpoint it performs a GET (optionally with extra request headers) and derives the age from one of:

- **`age_header`** — value of the response header `Age` (e.g. CloudFront edge cache age).
- **`date_header:<HeaderName>`** — parses the named response header as an HTTP date (RFC 2822 or ISO 8601) and reports `now - that`. Defaults to `Last-Modified` when no name is given.
- **`json_path:<dotted.path>`** — JSON-decodes the response body and resolves a dotted path (segments separated by `.`, list indices like `items[0]`). The value at that path is parsed as an ISO 8601 / RFC 2822 date or as a raw number of seconds.

The output is one JSON object per endpoint under section header `<<<endpoint_age:sep(0)>>>`.

The check plugin `endpoint_age` discovers one service per endpoint (`Endpoint age <name>`) and reports:

- `CRIT` when the endpoint is unreachable, returns an HTTP error or the configured age source cannot be extracted (e.g. JSON path not found, header missing, body not JSON).
- Otherwise: result of applying `SimpleLevels` (WARN/CRIT upper) to the age, plus an `endpoint_age` metric so the freshness can be graphed.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/endpoint_age/libexec/agent_endpoint_age` | Python special agent that probes endpoints and extracts the age. |
| `src/endpoint_age/server_side_calls/agent.py` | Builds the command line from the WATO rule. |
| `src/endpoint_age/rulesets/agent.py` | WATO form for the special agent (endpoint list, source, optional headers, timeout). |
| `src/endpoint_age/rulesets/endpoint_age.py` | WATO form for the WARN/CRIT thresholds. |
| `src/endpoint_age/agent_based/endpoint_age.py` | Section parser, discovery and check function. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a Checkmk host (any agent type — special agents do not need a real agent on the host).
3. Configure the special agent rule for the host.

## Configuration

Rule: **Setup → Agents → Other integrations → Endpoint age (HTTP freshness)**

Per endpoint:

| Parameter | Type | Meaning |
| --- | --- | --- |
| `name` | String (required) | Item name in the resulting `Endpoint age <name>` service. |
| `url` | URL (required) | URL to probe. |
| `source` | Choice (required) | One of `age_header`, `date_header:<HeaderName>`, `json_path:<dotted.path>`. |
| `timeout` | Float seconds (optional, default 15) | Per-endpoint HTTP timeout. |
| `extra_headers` | List of `Name: Value` strings (optional) | Sent with the GET request. Useful for auth tokens or for overriding the default User-Agent on APIs that block non-browser clients. |

Rule: **Setup → Services → Service monitoring rules → Endpoint age (HTTP freshness)**

| Parameter | Type | Default | Meaning |
| --- | --- | --- | --- |
| `max_age` | SimpleLevels (TimeSpan, upper) | 15 minutes WARN / 60 minutes CRIT | Applied to the extracted age. |

## Caveats

- `age_header` measures **edge cache age**, not data freshness. If an upstream producer stops but the origin still serves the (now stale) data, a CDN like CloudFront will keep refetching it within its `max-age` window and reset `Age` to 0 — the check stays green while the data is stale. Use `json_path` against a real `last_updated`/`generated_at` field in the response when reliable freshness is required.
- `extra_headers` can override the default `User-Agent` (`checkmk-endpoint-age/1.0`). Some AWS-fronted endpoints reject non-browser User-Agents; setting `User-Agent: Mozilla/5.0 (compatible; checkmk)` is usually enough.
