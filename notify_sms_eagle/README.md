# SMS Eagle Notification

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p13-blue)
<!-- compatibility-badges:end -->

Checkmk notification plugin that sends host/service alerts as SMS via
an SMS Eagle appliance using its v2 HTTP API and token authentication.
Optionally includes a configured host or service label in the SMS
text.

## How it works

The notification script `sms_eagle` is invoked by Checkmk with the
usual notification context. It POSTs a JSON payload to
`<api_host>/api/v2/messages/sms_single` with the `access-token` header:

```text
{"to": "<CONTACTPAGER>", "text": "<hostname> [SL key:value] [HL key:value] <state> <output>"}
```

The message is built from the host name, an optional matching
service/host label, and the current host or service state plus output,
truncated to 160 characters.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/notifications/sms_eagle` | Notification script (Python, uses `requests`). |
| `src/sms_eagle/rulesets/notification_parameter.py` | Registers notification parameter `sms_eagle` via `notification_parameter_registry`. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a notification rule in *Setup -> Notifications* and pick
   *SMS Eagle SMS Appliance* as the method.
3. Supply an API token created on the SMS Eagle appliance.

## Configuration

Notification parameters (`sms_eagle`):

| Parameter | Type | Meaning |
| --- | --- | --- |
| `api_host` | String | Base URL of the SMS Eagle API, e.g. `https://eagle.example.com`. |
| `api_token` | Password | v2 API access token. |
| `svc_label` | String (optional) | Service label key whose value will be embedded in the SMS. |
| `host_label` | String (optional) | Host label key whose value will be embedded in the SMS. |
| `ssl_verify` | BooleanChoice (default: true) | Verify the appliance TLS certificate. Disable for self-signed certs. |

The recipient's phone number is taken from the Checkmk contact's
pager address (`CONTACTPAGER`). If empty, the plugin exits with state
2.

## Known limitations

- The ruleset file still bridges into the legacy valuespec via
  `recompose(...)` / `notification_parameter_registry` because of the
  mixed Form Spec / legacy notification parameter setup in Checkmk
  2.4.
