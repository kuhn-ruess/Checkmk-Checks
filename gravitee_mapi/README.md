# Gravitee API Management Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p18-blue)
<!-- compatibility-badges:end -->

Special agent for Gravitee API Management (MAPI). Discovers every API in the configured Gravitee environment and produces three services per API: average response time, error rate distribution, and availability / health.

## How it works

The special agent [`agent_gravitee_mapi`](src/gravitee_mapi/libexec/agent_gravitee_mapi) authenticates against the Gravitee MAPI with a bearer token and calls the Management v2 API:

- `GET /management/v2/environments/{env}/apis/` — list all APIs.
- `GET /management/v2/environments/{env}/apis/{id}/analytics?type=STATS&field=gateway-response-time-ms` — response time stats over the configured interval.
- `GET /management/v2/environments/{env}/apis/{id}/analytics/response-status-ranges` — HTTP status code histogram.
- `GET /management/v2/environments/{env}/apis/{id}/health/availability` — availability percentage.

The results per API are emitted as one JSON line in the `<<<gravitee_mapi:sep(0)>>>` section. The check plugins in [`apis.py`](src/gravitee_mapi/agent_based/apis.py) parse that section keyed by API name and produce:

- `gravitee_mapi_stats` — `API <name> Response Time`; reports requests count plus avg/min/max response time with `check_levels`.
- `gravitee_mapi_errors` — `API <name> Error Rates`; counts 2xx/4xx/5xx, WARN on any 4xx, CRIT on any 5xx.
- `gravitee_mapi_health` — `API <name> Health`; OK >= 99%, WARN >= 95%, otherwise CRIT.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/gravitee_mapi/libexec/agent_gravitee_mapi` | Special agent script (Python, uses `requests`). |
| `src/gravitee_mapi/server_side_calls/agent.py` | Builds the agent command line from WATO params. |
| `src/gravitee_mapi/rulesets/agent.py` | WATO rule *Gravitee API Management*. |
| `src/gravitee_mapi/agent_based/apis.py` | Section parser plus the three check plugins. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a bearer token in Gravitee with permission to read APIs, analytics and health.
3. Create the WATO rule *Setup -> Agents -> Other integrations -> Gravitee API Management* for the Gravitee host.
4. Run service discovery.

## Configuration

Rule: **Setup -> Agents -> Other integrations -> Gravitee API Management**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `token` | Password | Bearer token for MAPI authentication. |
| `environment` | String | Gravitee environment name (default `DEFAULT`). |
| `interval` | Integer seconds | Time range used for analytics queries. Should match the Checkmk check interval (minimum 10, default 60). |
| `no_verify_ssl` | Boolean | Disable TLS certificate verification. |

The host name is taken from the Checkmk host configuration (`host_config.name`).

## Services & metrics

- **`API <name> Response Time`** — metrics `response_time`, `response_time_min`, `response_time_max`.
- **`API <name> Error Rates`** — metrics `requests_2xx`, `requests_4xx`, `requests_5xx`, `requests_total`; WARN on any 4xx, CRIT on any 5xx.
- **`API <name> Health`** — metric `availability` (percent); thresholds 99 / 95.
