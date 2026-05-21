# AWS service status RSS monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.4.0-blue)
<!-- compatibility-badges:end -->

Special agent that probes the per-service status RSS/Atom feeds published by AWS at <https://status.aws.amazon.com/>. For every configured feed the check verifies that the feed is reachable, contains valid XML, and reports the age of the most recent published event.

## How it works

The agent script `agent_aws_status_rss` takes one or more `--feed "Name=URL"` arguments plus an optional `--timeout` (seconds, default 15) and, for each feed:

<img width="2358" height="1868" alt="grafik" src="https://github.com/user-attachments/assets/d9abc0ad-335e-40db-9946-142f5637e881" />


1. Performs a GET against the feed URL with `User-Agent: checkmk-aws-status-rss/1.0`.
2. Parses the response as RSS 2.0 (`<item>`) or Atom (`<entry>`), extracts every item's title, published date and summary.
3. Sorts items newest-first and reports reachability, item count, latest title/date/summary and the age of the latest entry in seconds.

The output is emitted as one JSON object per feed under section header `<<<aws_status_rss:sep(0)>>>`.

The check plugin `aws_status_rss` discovers one service per feed (`AWS Status <name>`) and reports:

<img width="2262" height="1096" alt="grafik" src="https://github.com/user-attachments/assets/68f08e9b-3ad9-4334-87e0-e28ed52ea1a6" />


- `CRIT` when the feed cannot be fetched or parsed (HTTP error, timeout, non-XML response — this catches the "RSS Antwort liefert keine Daten" case).
- `OK` when the feed is healthy and contains no items (= AWS reports no incident for the service).
- `WARN` / `CRIT` when the most recent entry is younger than the configured thresholds (an event has just been published).

## Package contents

| Path | Purpose |
| --- | --- |
| `src/aws_status_rss/libexec/agent_aws_status_rss` | Python special agent that fetches and parses RSS/Atom feeds. |
| `src/aws_status_rss/server_side_calls/agent.py` | Builds the command line from the WATO rule. |
| `src/aws_status_rss/rulesets/agent.py` | WATO form for the special agent (feed list + timeout). |
| `src/aws_status_rss/rulesets/aws_status_rss.py` | WATO form for the check thresholds. |
| `src/aws_status_rss/agent_based/aws_status_rss.py` | Section parser, discovery and check function. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a Checkmk host for the AWS status monitoring (any agent type — special agents do not need a real agent on the host).
3. Configure the special agent rule for the host.

## Configuration

Rule: **Setup → Agents → Other integrations → AWS service status RSS**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `feeds` | List of `{name, url}` (required) | Service name (used as item) and feed URL. |
| `timeout` | Float seconds (optional, default 15) | Per-feed HTTP timeout. |

Rule: **Setup → Services → Service monitoring rules → AWS service status RSS**

| Parameter | Type | Default | Meaning |
| --- | --- | --- | --- |
| `event_age_warn` | TimeSpan | 7 days | WARN if the newest event is younger than this. |
| `event_age_crit` | TimeSpan | 1 day | CRIT if the newest event is younger than this. |

## Example

```
Amazon CloudFront     = https://status.aws.amazon.com/rss/cloudfront.rss
Amazon API Gateway    = https://status.aws.amazon.com/rss/apigateway-eu-central-1.rss
AWS Lambda            = https://status.aws.amazon.com/rss/lambda-eu-central-1.rss
Amazon RDS            = https://status.aws.amazon.com/rss/rds-eu-central-1.rss
AWS Step Functions    = https://status.aws.amazon.com/rss/state-eu-central-1.rss
AWS NAT Gateway       = https://status.aws.amazon.com/rss/natgateway-eu-central-1.rss
Amazon S3             = https://status.aws.amazon.com/rss/s3-eu-central-1.rss
Amazon CloudWatch     = https://status.aws.amazon.com/rss/cloudwatch-eu-central-1.rss
```
