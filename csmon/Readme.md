# CSMON SAP Monitoring Connector

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p18-blue)
<!-- compatibility-badges:end -->

Special agent that imports hosts and services from a CSMON SAP monitoring instance into Checkmk using the CSMON REST API. Each CSMON host is re-published as a piggyback block, and each CSMON service is emitted as a `local` check so it shows up natively under the corresponding Checkmk host.

## How it works

The special agent `agent_csmon` calls `https://<host>/api/monitoring/services?...&page=0&size=50000` with HTTP basic auth and walks the result once. For every row it:

1. Opens a piggyback block `<<<<<hostname>>>>` (once per host) and emits a `<<<local>>>` line for the host state with description and address.
2. Emits a `<<<local>>>` line per service using `performance_data` mapped to Checkmk perf format (`key=current;warn;crit;min;max`).
3. Maps CSMON states `OK/WARNING/CRITICAL/UNKOWN` to `0/1/2/3` and `UP/DOWN` to `0/2`.

The agent prints a minimal `<<<check_mk>>>` header identifying itself as `csmon connector`. Host creation happens in Checkmk through Dynamic Host Management against the piggyback data.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/csmon/libexec/agent_csmon` | Special agent, queries CSMON REST API and emits piggyback + local checks. |
| `src/csmon/rulesets/agent.py` | Special agent rule (username, password). |
| `src/csmon/server_side_calls/agent.py` | Maps params to the agent command line and passes the host name from `HostConfig`. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a collector host in Checkmk for the CSMON server, configure the special agent rule, then set up a piggyback folder and Dynamic Host Management so that the incoming CSMON hosts are materialised as Checkmk hosts.

## Configuration

Rule: **Setup -> Agents -> Other integrations -> CSMON Connector**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `username` | String | CSMON API user. |
| `password` | Password | CSMON API password. |

The collector host name itself is used as the CSMON hostname passed to the API.

## Known limitations

- SSL verification is hardcoded to `True` in the script via a module-level `ssl_verify` constant.
- A single page of 50000 services is fetched; larger environments will need an agent change.
- When upgrading from an earlier 1.x version the existing config should be removed and re-created on Checkmk 2.3.
