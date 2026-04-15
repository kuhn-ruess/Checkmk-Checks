# Arcgis Portal Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p18-blue)
<!-- compatibility-badges:end -->

Special agent for Esri ArcGIS Portal. Authenticates against the portal via `generateToken` and queries the REST API for IdP federation settings and certificate information. Early-stage package: the agent collects data, the check plugin is currently a placeholder.

## How it works

The agent script `agent_arcgis_portal` takes `--host-name`, `--username`, `--password` and optional `--proxy-url` and:

1. POSTs `username` + `password` (with `client=requestip`) to `https://<host>/portal/sharing/rest/generateToken` and stores the returned token.
2. GETs `https://<host>/sharing/rest/portals/self/idp/federation` and prints the raw JSON response.
3. GETs `https://<host>/sharing/rest/portals/self/idp/certificates` and prints the raw JSON response.

The check plugin `arcgis_certificates` registers an `AgentSection` called `arcgis_certificates` and a `Certificate` service, but the current check function only yields a placeholder `Hello World` result.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/arcgis_portal/libexec/agent_arcgis_portal` | Python special agent that talks to the ArcGIS REST API. |
| `src/arcgis_portal/server_side_calls/agent.py` | Builds the command line and forwards credentials. |
| `src/arcgis_portal/rulesets/agent.py` | WATO form: username, password, optional proxy URL. |
| `src/arcgis_portal/agent_based/certificates.py` | Placeholder certificate check plugin. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a Checkmk host for the portal and configure the special agent rule below.

## Configuration

Rule: **Setup → Agents → Other integrations → ArcGIS Portal**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `username` | String (required) | Portal user for `generateToken`. |
| `password` | Password (required) | Password for the portal user. |
| `proxy_url` | String (optional) | HTTP(S) proxy URL, e.g. `http://proxy.example.com:8080`. |

## Known limitations

- The `certificates` check plugin is a stub: it discovers a `Certificate` service but the check function only returns a `Hello World` result. The special agent already dumps federation and certificate JSON, so a real parser has to be added.
