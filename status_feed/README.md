# Status RSS/Atom feed monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-2.5-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0-blue)
<!-- compatibility-badges:end -->

Special agent that probes status RSS/Atom feeds. It works with the per-service status feeds published by AWS at <https://status.aws.amazon.com/> **and** with Statuspage-style incident-history feeds such as <https://status.scrivito.com/incidents.atom>. For every configured feed the check verifies that the feed is reachable, contains valid XML, reports the age of the most recent published event and classifies its incident state.

> Generalised successor of `aws_status_rss`. The plugin id, section, service name and rules were renamed from `aws_status_rss` (service `AWS Status %s`) to `status_feed` (service `Status feed %s`). Existing `aws_status_rss` rules and discovered services do **not** migrate automatically — reconfigure the special agent rule and rediscover after switching.

## How it works

The agent script `agent_status_feed` takes one or more `--feed "Name=URL"` arguments plus an optional `--timeout` (seconds, default 15) and `--user-agent` and, for each feed:

1. Performs a GET against the feed URL (default `User-Agent: checkmk-status-feed/1.0`).
2. Parses the response as RSS 2.0 (`<item>`) or Atom (`<entry>`); for Atom the text is taken from `<summary>` or, if absent, `<content>` (Statuspage feeds use `<content>`).
3. Sorts items newest-first and reports reachability, item count, latest title/date/summary, the age of the latest entry, and a classified incident state (`active` / `resolved` / `unknown`) derived from lifecycle keywords in the newest entry.

The output is emitted as one JSON object per feed under section header `<<<status_feed:sep(0)>>>`.

The check plugin `status_feed` discovers one service per feed (`Status feed <name>`) and supports two evaluation modes:

- **Age mode** (default, for AWS per-service feeds): `OK` when the feed is valid and empty (no incident), `WARN`/`CRIT` when the newest entry is younger than the configured thresholds (an event is in flight).
- **Incident mode** (for Statuspage-style history feeds that keep resolved incidents forever, e.g. Scrivito): the lifecycle of the newest entry decides — a `resolved` entry is `OK` regardless of age, an `active` incident raises the configured state (default `CRIT`).

In both modes the service goes `CRIT` when the feed cannot be fetched or parsed (HTTP error, timeout, non-XML response — this catches the "feed liefert keine Daten" case).

## Package contents

| Path | Purpose |
| --- | --- |
| `src/status_feed/libexec/agent_status_feed` | Python special agent that fetches and parses RSS/Atom feeds. |
| `src/status_feed/server_side_calls/agent.py` | Builds the command line from the WATO rule. |
| `src/status_feed/rulesets/agent.py` | WATO form for the special agent (feed list, timeout, user-agent). |
| `src/status_feed/rulesets/status_feed.py` | WATO form for the check (mode + thresholds). |
| `src/status_feed/agent_based/status_feed.py` | Section parser, discovery and check function. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a Checkmk host for the status monitoring (any agent type — special agents do not need a real agent on the host).
3. Configure the special agent rule for the host.

## Configuration

Rule: **Setup → Agents → Other integrations → Status RSS/Atom feeds**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `feeds` | List of `{name, url}` (required) | Feed name (used as item) and feed URL. |
| `timeout` | Float seconds (optional, default 15) | Per-feed HTTP timeout. |
| `user_agent` | String (optional) | User-Agent header; some endpoints reject the default. |

Rule: **Setup → Services → Service monitoring rules → Status RSS/Atom feeds**

| Parameter | Type | Default | Meaning |
| --- | --- | --- | --- |
| `incident_mode` | Choice `age` / `incident` | `age` | Evaluation mode (see above). |
| `active_incident_state` | Service state | `CRIT` | State on an active incident (incident mode only). |
| `event_age_warn` | TimeSpan | 7 days | WARN if the newest event is younger than this (age mode). |
| `event_age_crit` | TimeSpan | 1 day | CRIT if the newest event is younger than this (age mode). |

## Examples

AWS per-service feeds (age mode):

```
Amazon CloudFront     = https://status.aws.amazon.com/rss/cloudfront.rss
Amazon API Gateway    = https://status.aws.amazon.com/rss/apigateway-eu-central-1.rss
AWS Lambda            = https://status.aws.amazon.com/rss/lambda-eu-central-1.rss
Amazon RDS            = https://status.aws.amazon.com/rss/rds-eu-central-1.rss
Amazon S3             = https://status.aws.amazon.com/rss/s3-eu-central-1.rss
Amazon CloudWatch     = https://status.aws.amazon.com/rss/cloudwatch-eu-central-1.rss
```

Statuspage-style incident-history feed (incident mode):

```
Scrivito              = https://status.scrivito.com/incidents.atom
```
