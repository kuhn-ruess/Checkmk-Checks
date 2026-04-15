# Rediscover service

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p5-blue)
<!-- compatibility-badges:end -->

Notification plugin that triggers a service rediscovery via the Checkmk REST API whenever a matching service notification fires. Useful for items that legitimately change at runtime (mount options, interface speed, SMART attributes, ...) so that the stored discovery parameters are refreshed automatically instead of requiring a manual rediscovery.

## How it works

On each service notification the script reads the site's `automation` secret from `~/var/check_mk/web/automation/automation.secret` and calls the REST API against the configured Checkmk host and site:

1. `GET /objects/service_discovery/<host>` to look up the affected service entry in the check table.
2. `PUT /objects/host/<host>/actions/update_discovery_phase/invoke` — first to move the service to `undecided`, then again with `target_phase=monitored` to re-add it with the current discovery values.
3. `POST /domain-types/activation_run/actions/activate-changes/invoke` with `force_foreign_changes=true` to activate the change.

The plugin only runs for `NOTIFY_WHAT=SERVICE`; host notifications are ignored.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/notifications/rediscover_service` | Notification script executed by Checkmk. |
| `src/redis_service/rulesets/redis_service.py` | WATO notification parameter form (protocol, hostname, site name). |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a new notification rule and select *Rediscover service* as the plugin.
3. Provide the Checkmk server hostname and site name that the REST API call should target (use the central/master site in a distributed setup).
4. Select a user with automation rights (e.g. `cmkadmin`) as the contact for the rule. The script itself authenticates as `automation` using the site secret.
5. Restrict the rule to the hosts and services that should be auto-rediscovered (typically with a service state condition).

## Configuration

Rule: **Notifications -> Rediscover service**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `proto` | `http` / `https` | Protocol used to reach the Checkmk REST API. |
| `hostname` | String | Hostname of the Checkmk (master) server. |
| `sitename` | String | Name of the Checkmk site. |

## Known limitations

- The script must run on a site where `~/var/check_mk/web/automation/automation.secret` exists and is readable, and that site must have permission to activate foreign changes.
- Only service notifications are processed; host-level changes are not rediscovered.
- Activation is forced (`force_foreign_changes=true`) and applies to all sites.
