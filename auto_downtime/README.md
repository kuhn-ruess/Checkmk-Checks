# Automatic downtime and acknowledgement

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.5.0p16-blue)
<!-- compatibility-badges:end -->

Looks at the summary (plugin output) of services. When service name and a text in the
summary match a configured rule, it schedules a downtime for the service, acknowledges
its problem, removes its existing downtimes or acknowledgement, or combines these. The downtime duration,
the acknowledgement options and a comment filter for the downtimes to remove are set
per rule.

Typical use: a check reports a known, harmless condition (for example a planned
maintenance message of an application) and the service should be silenced for a while
without anyone touching it. When the application reports the end of the maintenance,
the downtime is removed again.

The package offers two ways to run it, both with the same rules:

| Mode | Rule | Acts | Talks to |
| --- | --- | --- | --- |
| Active check | *Setup > Services > Other services > Automatic downtime and acknowledgement by plugin output* | on all services of the site, on every check interval | REST API, automation user |
| Notification plugin (action handler) | *Setup > Notifications > Parameters for notification methods > Automatic downtime and acknowledgement*, used as method in a notification rule | on the notified service, right when the problem notification is created | local Livestatus |

The notification plugin acts the moment the problem is notified, without waiting for a
check interval. Other notifications of that same event (for example mails) still go out,
later ones are suppressed by the downtime or acknowledgement. The active check also finds
services that do not notify, can end running downtimes and can filter by host name.

## Active check

### How it works

On every check interval the active check `check_auto_downtime` uses the Checkmk REST
API with an automation user:

1. `POST /domain-types/service/collections/all` reads host name, service name, state,
   summary, downtime depth, downtimes and acknowledgement state of all services.
2. For each service all rules are checked where
   * the host name matches *Host name* (optional, match from the start),
   * the service name matches *Service name* (match from the start, like service
     conditions in Checkmk) and
   * the *Text in the summary* regular expression is found anywhere in the summary.
3. All matching rules apply. If several of them have the same action, or opposite
   actions (schedule and remove a downtime, acknowledge and remove the acknowledgement),
   the first of them wins. The actions:

| Action | REST endpoint | Skipped when |
| --- | --- | --- |
| Downtime | `POST /domain-types/downtime/collections/service`, fixed, from now for the configured duration | the service is already in a downtime |
| Remove downtimes | `POST /domain-types/downtime/actions/delete/invoke` with the IDs of the downtimes whose comment matches the filter | the service has no such downtime |
| Acknowledgement | `POST /domain-types/acknowledge/collections/service`, sticky, persistent comment, notification, optional expiry | the service is OK or already acknowledged |
| Remove acknowledgement | `POST /domain-types/acknowledge/actions/delete/invoke` | the service is not acknowledged |

So nothing is set twice on the next check interval. When a downtime has ended and the
summary still matches, a new downtime is set.

The service of the active check itself is skipped.

### Service state

| Situation | State |
| --- | --- |
| Services queried, all actions worked (or nothing to do) | OK |
| At least one downtime or acknowledgement failed (for example missing permission) | CRIT |
| Services cannot be queried (URL, login, secret, regular expression) | UNKNOWN |

Summary: `5 matching services, 2 downtimes set, 1 downtimes removed, 2 acknowledged,
3 already handled`. The details list every matching service and what happened to it.
Metrics: `matched`, `downtimes`, `removed`, `acknowledged`, `handled`, `errors`.

## Notification plugin

The script `auto_downtime` handles service notifications of type `PROBLEM` only, host
notifications and other types are ignored. It matches service name and summary of the
notified service against the rules, all matching rules apply like in the active check
(without *Remove acknowledgement*, a problem notification is not acknowledged), and sends the commands
to the local Livestatus: `SCHEDULE_SVC_DOWNTIME`, `ACKNOWLEDGE_SVC_PROBLEM`,
`DEL_SVC_DOWNTIME`. Like the active check it skips a downtime when the service is already
in one and an acknowledgement when it is already acknowledged. The result is written to
the notification log (`var/log/notify.log`) and the notification history of the service.

Checkmk sends no notifications while a service is in a downtime. *Remove downtimes* in a
notification rule therefore only removes downtimes that have not started yet, for
example a planned maintenance window that is no longer needed. To end a running downtime
when the summary changes, use the active check.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/auto_downtime/libexec/check_auto_downtime` | Active check executable. |
| `src/auto_downtime/server_side_calls/active_check.py` | Builds the command line. |
| `src/auto_downtime/rulesets/active_check.py` | Rule *Automatic downtime and acknowledgement by plugin output*. |
| `src/notifications/auto_downtime` | Notification plugin. |
| `src/auto_downtime/rulesets/notification_parameter.py` | Notification parameters *Automatic downtime and acknowledgement*. |

## Configuration

### Active check

1. Install the MKP.
2. Create an automation user, for example `auto_downtime`, with permission to see all
   services and to set downtimes and acknowledgements (for example role *Administrator*).
3. Store its secret in the password store (*Setup > General > Passwords*).
4. Create the rule *Setup > Services > Other services > Automatic downtime and
   acknowledgement by plugin output* for exactly one host, for example the Checkmk
   server itself. Every host the rule applies to gets its own check that acts on all
   services.
5. Activate the changes.

| Parameter | Meaning |
| --- | --- |
| Service name of this check | Name of the active check service, default `Auto downtime`. |
| Checkmk URL | Base URL of the site, for example `https://monitoring.example.com/mysite`. Default: the local site via its Apache port. |
| Automation user | User for the REST API. |
| Automation secret | Secret of the user, best from the password store. It is passed as password store reference, never in plain text on the command line. |
| Verify the SSL certificate | Default on. |
| Rules | List of rules, see below. |

Per rule:

| Parameter | Meaning |
| --- | --- |
| Host name | Optional regular expression for the host name, prefix match. |
| Service name | Regular expression for the service name, prefix match. `.*` matches all services. |
| Text in the summary | Regular expression searched in the summary of the service, case-sensitive. `(?i)` in front ignores the case. |
| Schedule a downtime | Enables the downtime. *Duration of the downtime* (minimum one minute). |
| Remove downtimes | Removes the downtimes of the service. *Only downtimes with comment*: regular expression searched in the downtime comment, empty removes all downtimes of the service. |
| Acknowledge the problem | Enables the acknowledgement. *Sticky*, *Persistent comment*, *Send acknowledgement notification*, *Expire after*. |
| Remove the acknowledgement | Active check only. Removes the acknowledgement of the service, for example when the summary reports that the acknowledged problem is gone. |
| Comment | Comment of downtime and acknowledgement. Default: names the matching regular expression. |

At least one action must be enabled. *Schedule a downtime* and *Remove downtimes* exclude
each other within one rule, as do *Acknowledge the problem* and *Remove the
acknowledgement*; every other combination is fine. Author of downtimes and
acknowledgements is the automation user.

Example: rule 1 with service name `Application `, text in the summary
`maintenance finished` and *Remove downtimes* with comment filter `^Automatic`; rule 2 with
the same service name, text `maintenance (planned|active)`, downtime of 2 hours,
acknowledgement sticky. Both rules may match the same service, then both apply. With the
comment filter, downtimes set by hand stay untouched.

Example for Checkmk BI aggregations, whose summary reads `In downtime: yes/no,
Acknowledged: yes/no`: one rule each for `In downtime: yes` (downtime),
`In downtime: no` (remove downtimes with the comment of the first rule),
`Acknowledged: yes` (acknowledge) and `Acknowledged: no` (remove the acknowledgement).
Every aggregation matches two of them, so downtime and acknowledgement follow the
aggregation in both directions.

### Notification plugin

1. Install the MKP.
2. *Setup > Notifications > Parameters for notification methods > Automatic downtime and
   acknowledgement*: create a parameter set with the rules. Same rule options as above,
   without *Host name*; use the conditions of the notification rule for that. Optional
   *Author of downtime and acknowledgement*, default `auto_downtime`.
3. Create a notification rule with this method and parameter set, conditions for the
   services, and a contact (for example a single admin user), since notification
   plugins only run for a contact. Put it before the rules that send mails.
4. Activate the changes.

## Known limitations

* The active check acts on its own interval. Between the state change of a service and the next
  run of the check, notifications for that service can still go out. Delay the
  notification rules for these services (condition *Delay execution for n minutes*) or
  run the check more often.
* Only the summary is searched, not the long output (details).
* Expiring acknowledgements need the Checkmk Micro Core (commercial editions).
* In a distributed setup, point *Checkmk URL* to the central site to cover all sites. The
  notification plugin acts on the site that creates the notification.
* The notification plugin handles service problems only, no host notifications.
