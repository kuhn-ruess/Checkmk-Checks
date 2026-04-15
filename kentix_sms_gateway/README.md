# Kentix SMS Gateway notification

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.1.0p9-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.1.0-blue)
<!-- compatibility-badges:end -->

Bulk-capable Checkmk notification plugin that sends SMS messages through a Kentix AlarmManager's built-in SMS gateway. The notification target is the contact's pager number.

## How it works

The notification script calls the Kentix AlarmManager HTTP endpoint:

```text
https://<manager_ip>/php/sms_gateway.php?key=<password>&recipients=<pager>&message=<text>
```

It reads the contact context (bulk or single) via `cmk.notification_plugins.utils`, retrieves the gateway password from the password store, URL-encodes the pager number and the message, and submits the request. HTTP response codes are mapped to error messages:

| Code | Meaning |
| --- | --- |
| `200` | delivered |
| `403` | wrong SMS gateway password |
| `404` | SMS gateway not active |
| `900` | SIM card not recognized |
| `901` | GSM modem not detected |
| `902` | SIM card locked |

Bulk mode (`--bulk`) is supported and builds a single subject line covering all hosts in the bulk.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/notifications/kentix` | Notification script (Python, `Bulk: yes`). |
| `src/web/plugins/wato/notification_sms_kentix.py` | WATO ruleset `NotificationParameterKentix` (ident `kentix`). |

## Installation

1. Install the MKP on the Checkmk site.
2. Configure each contact who should receive SMS with a pager number (E.164 format, spaces are stripped).
3. Create a notification rule of type *Kentix SMS Gateway* and fill in the parameters below.

## Configuration

WATO rule: **Setup -> Notifications** -> notification method *Kentix SMS Gateway*.

| Parameter | Type | Meaning |
| --- | --- | --- |
| `ipaddress` | IPv4Address | IP of the Kentix AlarmManager exposing the SMS gateway. |
| `password` | Password (stored) | SMS gateway password (the `key` URL parameter). |
| `template_text` | Text area | Message body; Checkmk context macros are substituted before sending. |

## Known limitations

- Uses the legacy `cmk.gui.plugins.wato.utils` / `notification_parameter_registry` API. Still loads on 2.1 and later as long as the legacy notification API is available.
- The WATO module references `Dictionary` and `_` without explicit imports — this follows the original 2.1 convention where those names are provided implicitly by the WATO loader.
- SMS delivery uses plain HTTPS with no certificate verification configuration.
