# Veritas Flex Appliance

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p25-blue)
<!-- compatibility-badges:end -->

Special agent for Veritas Flex storage appliances. Logs in against the Flex REST API, reads node hardware and services health, and enumerates instances; the results are emitted as a `<<<local>>>` section, so each check is a Checkmk local check.

## How it works

1. POST to `https://<host>/api/v1/login` with username/password, token with TTL 30, stored as `X-Auth-Token`.
2. GET `v1/nodes` to enumerate cluster nodes.
3. For every node: GET `v1/nodes/<node>/health/hardware` and `v1/nodes/<node>/health/services`. A two-key response body is treated as healthy (state 0); anything else is degraded (state 2).
4. GET `v3/instances` and emit one local check per instance — OK when `status == ONLINE`, CRIT otherwise.
5. All output is printed below a single `<<<local>>>` section header in the legacy local-check line format.

```text
<<<local>>>
0 "node01 Hardware Health" - Hardware is healthy
0 "node01 Services Health" - Services are healthy
0 instance01 - is ONLINE
```

## Package contents

| Path | Purpose |
| --- | --- |
| `src/veritas_flex/libexec/agent_veritas` | Special agent (Python, uses `requests`). |
| `src/veritas_flex/rulesets/agent.py` | WATO `SpecialAgent` rule *Veritas Flex Appliance* (topic *Storage*). |
| `src/veritas_flex/server_side_calls/veritas.py` | Builds the command: `<api_url> -u <user> -p <password>`. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create an API user on the Flex appliance.
3. Add the appliance as a host in Checkmk and create a *Veritas Flex Appliance* special agent rule for it.
4. Discovery creates one service per hardware/services health report and one per instance, all driven by the standard local check plugin.

## Configuration

WATO rule: *Setup > Agents > Other integrations > Veritas Flex Appliance*.

| Parameter | Type | Meaning |
| --- | --- | --- |
| `api_url` | String (required) | Hostname or host:port used in `https://<api_url>/api/`. |
| `username` | String (required) | Flex API user. |
| `password` | Password (required) | Flex API password. |

## Known limitations

- Health evaluation is naive: the code only counts top-level JSON keys in the response (`len(json_body.keys())`) to decide healthy vs degraded, with no inspection of actual fault details.
- The agent logs into `/tmp/checkMK_flex.log` on the Checkmk site and does not call `do_logout()`.
- All results flow through `<<<local>>>`, so there is no dedicated check plugin, ruleset or metric — configuration must happen via the standard *Local checks* rules.
