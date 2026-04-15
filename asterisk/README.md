# Asterisk notification script

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p20-blue)
<!-- compatibility-badges:end -->

Notification script that places a phone call via an Asterisk PBX when Checkmk raises a notification. Uses the Asterisk Manager Interface (AMI) `Originate` action to dial a configured channel / extension.

## How it works

The script [`notifications/asterisk`](src/notifications/asterisk) collects the notification context, logs in to the AMI endpoint with `asterisk.ami.AMIClient`, issues an `Originate` action with the configured channel, extension, context, priority and caller ID, and then logs off. If the Python package `asterisk-ami` is missing the script exits with a clear error.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/notifications/asterisk` | Notification script invoked by Checkmk. |
| `src/asterisk/rulesets/asterisk.py` | WATO notification parameter form (legacy `cmk.gui.plugins.wato` API). |

## Installation

1. Install the MKP on the Checkmk site.
2. As the site user, install the required Python package: `pip3 install "asterisk-ami>=0.1.7"`.
3. In Checkmk create a notification rule using *Asterisk* and fill in the parameters below.

## Configuration

Rule: **Setup -> Notifications -> Notification rule -> Notification Method: Asterisk**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `host` | Text | IP address of the Asterisk server. |
| `port` | Integer | AMI port (default `5038`). |
| `timeout` | Integer | AMI timeout in seconds (default `180`, must exceed expected call duration). |
| `username` | Text | AMI user with `call`, `command` and `originate` privileges. |
| `password` | Password | AMI password (individual or stored). |
| `channel` | Text | Channel used for calling (e.g. `SIP/trunk`). |
| `exten` | Text | Extension to dial. |
| `priority` | Integer | Dialplan priority (default `1`). |
| `context` | Text | Dialplan context. |
| `callerid` | Text | Caller ID used for the outgoing call. |

## Known limitations

- The ruleset uses the pre-2.3 `notification_parameter_registry` API; it still loads on 2.3 / 2.4 as long as the legacy API is available.
- The script sends a call only, it does not speak the notification content; pairing it with a dialplan that plays a message is up to the Asterisk side.
