# Cherwell notification script

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p7-blue)
<!-- compatibility-badges:end -->

Notification script that creates incidents in Ivanti Service Management (formerly Cherwell). It posts the notification context to the Cherwell REST API, then performs a follow-up update and, for Event Console notifications, acknowledges the original event with the returned incident ID.

## How it works

The script [`notifications/cherwell_notify`](src/notifications/cherwell_notify):

1. Obtains an OAuth2 token from `token_url` using a password grant. The token is cached in `/opt/omd/sites/<site>/tmp/cherwell_token` for 15 minutes.
2. Builds a fixed Cherwell `busObId` payload (Incident business object with hardcoded customer and service fields) containing hostname, application, timestamp, severity, plugin output, counter, CMK-SLA, contacts and a direct link back to the Checkmk host / event view.
3. POSTs the payload to `api_url` to create the incident, extracts `busObPublicId` and then posts an update payload setting the incident `Herkunft = Ereignis` and `Status = Neu`.
4. For Event Console notifications (`SERVICECHECKCOMMAND` starts with `ec-rule-`), the script also acknowledges the event via the Checkmk REST API (`/objects/event_console/<EC_ID>/actions/update_and_acknowledge/invoke`) using an automation secret; on failure it falls back to writing a `COMMAND UPDATE` to the event daemon Unix socket.

`RECOVERY` notifications are explicitly not implemented and raise an exception.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/notifications/cherwell_notify` | Notification script. |
| `src/cherwell_notify/rulesets/cherwell_notify.py` | WATO notification parameter form (`cmk.rulesets.v1`). |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a dedicated Checkmk automation user and copy its secret into the notification rule as *Automation Secret of Checkmk*.
3. Create a notification rule using the *Cherwell notify* method and fill in the parameters below.

## Configuration

Rule: **Setup -> Notifications -> Notification rule -> Notification Method: Cherwell notify**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `api_url` | String | Full Cherwell REST API URL (incident endpoint). |
| `token_url` | String | Full Cherwell token endpoint. |
| `client_id` | String | OAuth client ID. |
| `username` | String | Cherwell API user. |
| `password` | Password | Password for the Cherwell API user. |
| `automation_secret` | Password | Checkmk automation user secret used to acknowledge EC events. |
| `cmk_server` | String | Checkmk server hostname (used to build links and REST calls). |
| `cmk_site` | String | Checkmk site name. |

## Known limitations

- SSL verification is disabled (`verify=False`) for all outbound Cherwell calls; `InsecureRequestWarning` is suppressed.
- The Cherwell `busObId` and all `fieldId` values are hardcoded to one specific customer tenant. Adapting this plugin to another Cherwell environment requires editing `build_payload_insert` / `build_payload_update`.
- `RECOVERY` notifications raise `Exception("Recovery not Implemented")` — only `PROBLEM` notifications are supported.
- The token cache path is hardcoded to `/opt/omd/sites/<site>/tmp/cherwell_token`.
