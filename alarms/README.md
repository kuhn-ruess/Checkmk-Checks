# Alarms

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p24-blue)
<!-- compatibility-badges:end -->

Notification plugin that plays an audible alarm through an HTTP API backend, for example to signal incidents on a TV, workstation or dedicated alarm box. Tested against a simple PHP backend shipped with XAMPP on Windows 11.

## How it works

On each notification, the script in `notifications/alarms` checks `NOTIFY_WHAT == SERVICE` and only fires when `NOTIFY_SERVICESTATE` is not `OK`. It then performs a `GET` against `{proto}://{hostname}/{url}?alarm={file}.mp3`, where the selected alarm name is mapped to a filename (`alarm1` -> `alarm-1.mp3`, `alarm2` -> `alarm-2.mp3`, `alarm3` -> `alarm-3.mp3`, `alarm4` -> `alarm-4.mp3`, `horse` -> `horse.mp3`). Exit code 0 on HTTP 200, 1 otherwise.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/notifications/alarms` | The notification script executed by Checkmk. |
| `src/alarms/rulesets/alarms.py` | WATO form for the notification parameters. |

## Installation

1. Deploy the HTTP backend that accepts the `?alarm=<file>` query parameter and plays the corresponding audio file on the target host (for example XAMPP on Windows 11 with a small PHP handler).
2. Install the MKP on the Checkmk site.
3. Create a notification rule that uses the `Play alarms (using API)` method and fill in the parameters below.

## Configuration

Rule: **Setup → Events → Notifications → Parameters for selected notification method → Play alarms (using API)**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `proto` | Choice (`http`, `https`) | Protocol used to reach the backend. Default `http`. |
| `hostname` | String | Host running the alarm backend. Default `localhost`. |
| `url` | String | Path of the API on the backend. Default `api.php`. |
| `alarm` | Choice (`alarm1`..`alarm4`, `horse`) | Which sound file to play. |

## Known limitations

- Only reacts to service notifications (`NOTIFY_WHAT == SERVICE`); host notifications are ignored.
- Sound filenames are hardcoded in the script; adding new entries requires editing both the ruleset and `notifications/alarms`.
