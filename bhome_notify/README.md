# BHome Notification

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p13-blue)
<!-- compatibility-badges:end -->

Notification script that forwards Checkmk host and service events to a BHome events API. Each notification is posted as a JSON payload to `https://<portal_domain>/events-service/api/v1.0/events` using a JWT obtained from `auth_api.login`.

## How it works

The script [`notifications/bhome_notify`](src/notifications/bhome_notify) collects the Checkmk notification context and builds a payload containing severity, message, source identifier, hostname, Checkmk problem ID, service level and a tag derived from the first contact group ending in `_ALARM`. For host notifications `DOWN` is mapped to `CRITICAL` and `UP` to `OK`. The script retries on failure with exponential backoff (up to 5 attempts, capped at 60 s).

Authentication uses the credentials from the notification rule (`id`, `access`, `secret`) and is handled by a separate `auth_api` module that must be importable at runtime.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/notifications/bhome_notify` | Notification script executed by Checkmk. |
| `src/bhome_notify/rulesets/notification_parameter.py` | WATO notification parameter form (`cmk.rulesets.v1`, registered via the legacy `notification_parameter_registry`). |

## Installation

1. Install the MKP on the Checkmk site.
2. Make sure an `auth_api` module providing `login(config)` is importable by the site user (the notification script imports it lazily).
3. Create a notification rule using the *BHome Events API* method and fill in the parameters below.

## Configuration

Rule: **Setup -> Notifications -> Notification rule -> Notification Method: BHome Events API**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `portal_domain` | String | Domain of the BHome events portal without scheme (e.g. `events.example.com`). |
| `id` | String | Client ID for authentication. |
| `access` | Password | Access key. |
| `secret` | Password | Secret. |
