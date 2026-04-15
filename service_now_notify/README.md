# Service Now Notification

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p7-blue)
<!-- compatibility-badges:end -->

Notification plugin that creates and closes ServiceNow incidents for Checkmk host and service events, using Checkmk contact groups to derive the ServiceNow assignment group. A contact group prefix of `SNOW_<number>_...` determines the assignment: the group with the highest number wins, and host or service custom attributes can override it explicitly.

## How it works

On `PROBLEM` notifications the script POSTs a JSON payload to
`<api_url>checkmk/incident/create` using HTTP Basic authentication. On `RECOVERY` it posts to `checkmk/incident/close`. Both endpoints are called through an optional HTTPS proxy.

Key payload fields:

- `QUELLEID`: `<site>|<host>[|<service>]`
- `FQDN`, `KURZBESCHREIBUNG` (plugin output), `SERVERITY` (state)
- `MP`: management pack dict with hostname/service/contacts
- `ASSIGNMENT`: picked from contact groups whose names start with `SNOW_`, comparing the numeric segment between the first two underscores. Default fallback is `SNOW_000_OS`.
- `ASSIGNMENT_GROUP`: overridden by the host custom attribute `HOST_SNOW_RESP_GRP` or the service custom attribute `SERVICE_SVC_SNOW_RESP_GRP_2` when present.
- `DISPOSITION`: derived from the service level (`0 -> Keine_Bereitschaft`, `10 -> Bereitschaft`).

Debug and error information is written to `~/var/log/snow_notify.log`.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/notifications/service_now_notify` | Notification script executed by Checkmk. |
| `src/service_now_notify/rulesets/service_now_notify.py` | WATO notification parameter form (API URL, user, password, proxy). |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a new notification rule and select *ServiceNow Notify* as the plugin.
3. Configure API URL (with trailing slash), basic auth credentials, and optional proxy.
4. Assign Checkmk contact groups following the `SNOW_<NN>_<name>` scheme so that the script can pick the right assignment group, or set the `SNOW_RESP_GRP` custom host/service attributes to override.

## Configuration

| Parameter | Type | Meaning |
| --- | --- | --- |
| `api_url` | String | Base URL of the ServiceNow integration endpoint (the script appends `checkmk/incident/create` or `checkmk/incident/close`). |
| `api_user` | String | HTTP Basic user. |
| `api_password` | Password | HTTP Basic password. |
| `proxy` | String | Optional HTTPS proxy. |

## Known limitations

- The ruleset uses the mixed legacy/new form-spec notification API (`recompose` + `notification_parameter_registry`) and will need adjustments if that compatibility shim is removed in a later Checkmk release.
- Payload field names are in German (`QUELLE`, `ZIEL`, `KURZBESCHREIBUNG`, ...) because they target a specific customer middleware — adjust the script if your ServiceNow bridge expects different keys.
- `DISPOSITION` only distinguishes two service levels (`0` and `10`); other values fall back to `N/A`.
- Only `PROBLEM` and `RECOVERY` notification types are handled; everything else exits silently.
