# Automatic downtime and acknowledgement

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.5.0p16-blue)
<!-- compatibility-badges:end -->

Active check that looks at the summary (plugin output) of the services of a Checkmk
site. When host name, service name and a text in the summary match a configured rule,
it schedules a downtime for the service, acknowledges its problem, or does both. The
downtime duration and the acknowledgement options are set per rule.

Typical use: a check reports a known, harmless condition (for example a planned
maintenance message of an application) and the service should be silenced for a while
without anyone touching it.

## How it works

On every check interval the active check `check_auto_downtime` uses the Checkmk REST
API with an automation user:

1. `POST /domain-types/service/collections/all` reads host name, service name, state,
   summary, downtime depth and acknowledgement state of all services.
2. For each service the rules are checked in order, the first one wins where
   * the host name matches *Host name* (optional, match from the start),
   * the service name matches *Service name* (match from the start, like service
     conditions in Checkmk) and
   * the *Text in the summary* regular expression is found anywhere in the summary.
3. The actions of the matching rule:

| Action | REST endpoint | Skipped when |
| --- | --- | --- |
| Downtime | `POST /domain-types/downtime/collections/service`, fixed, from now for the configured duration | the service is already in a downtime |
| Acknowledgement | `POST /domain-types/acknowledge/collections/service`, sticky, persistent comment, notification, optional expiry | the service is OK or already acknowledged |

So nothing is set twice on the next check interval. When a downtime has ended and the
summary still matches, a new downtime is set.

The service of the active check itself is skipped.

## Service state

| Situation | State |
| --- | --- |
| Services queried, all actions worked (or nothing to do) | OK |
| At least one downtime or acknowledgement failed (for example missing permission) | CRIT |
| Services cannot be queried (URL, login, secret, regular expression) | UNKNOWN |

Summary: `5 matching services, 2 downtimes set, 2 acknowledged, 3 already handled`.
The details list every matching service and what happened to it. Metrics: `matched`,
`downtimes`, `acknowledged`, `handled`, `errors`.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/auto_downtime/libexec/check_auto_downtime` | Active check executable. |
| `src/auto_downtime/server_side_calls/active_check.py` | Builds the command line. |
| `src/auto_downtime/rulesets/active_check.py` | Rule *Automatic downtime and acknowledgement by plugin output*. |

## Configuration

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
| Text in the summary | Regular expression searched in the summary of the service. |
| Schedule a downtime | Enables the downtime. *Duration of the downtime* (minimum one minute). |
| Acknowledge the problem | Enables the acknowledgement. *Sticky*, *Persistent comment*, *Send acknowledgement notification*, *Expire after*. |
| Comment | Comment of downtime and acknowledgement. Default: names the matching regular expression. |

At least one of *Schedule a downtime* and *Acknowledge the problem* must be enabled,
both together are fine. Author of downtimes and acknowledgements is the automation user.

Example: service name `Application `, text in the summary `maintenance (planned|active)`,
downtime of 2 hours, acknowledgement sticky.

## Known limitations

* The check acts on its own interval. Between the state change of a service and the next
  run of the check, notifications for that service can still go out. Delay the
  notification rules for these services (condition *Delay execution for n minutes*) or
  run the check more often.
* Only the summary is searched, not the long output (details).
* Expiring acknowledgements need the Checkmk Micro Core (commercial editions).
* In a distributed setup, point *Checkmk URL* to the central site to cover all sites.
