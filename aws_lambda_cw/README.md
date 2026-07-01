# AWS Lambda monitoring via CloudWatch

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![packaged](https://img.shields.io/badge/packaged-2.4.0-blue)
<!-- compatibility-badges:end -->

Special agent that monitors AWS Lambda functions through CloudWatch. Fetches
the core Lambda metrics (invocations, errors, throttles, duration) directly
from CloudWatch and creates one service per function.

## How it works

The agent script `agent_aws_lambda_cw` uses `boto3` to talk to CloudWatch:

1. Discovers Lambda functions via `cloudwatch:ListMetrics` (namespace
   `AWS/Lambda`), or uses an explicit list of function names from the rule.
2. Fetches per function over a configurable look-back window
   (`cloudwatch:GetMetricData`):
   - `Invocations` (Sum)
   - `Errors` (Sum)
   - `Throttles` (Sum)
   - `Duration` (Average and Maximum, in ms)
3. Emits one JSON object per function under section header
   `<<<aws_lambda_cw:sep(0)>>>`.

The check plugin `aws_lambda_cw` discovers one service per function
(`AWS Lambda <name>`) and reports invocations, errors (count and rate),
throttles and duration with configurable upper levels. By default the
service goes `WARN`/`CRIT` on one or more errors or throttles in the window.

> **Requirements:** `boto3` in the site Python (bundled with the Checkmk
> Enterprise/CEE-based editions) and an IAM identity with
> `cloudwatch:ListMetrics` and `cloudwatch:GetMetricData`. No Lambda or EC2
> permissions are required.
>
> If the access key itself carries no CloudWatch permissions and only assumes a
> (possibly cross-account) monitoring role, set `role_arn`: the key then needs
> `sts:AssumeRole` on that role, and the CloudWatch permissions live on the
> assumed role.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/aws_lambda_cw/libexec/agent_aws_lambda_cw` | Special agent (boto3 / CloudWatch). |
| `src/aws_lambda_cw/server_side_calls/agent.py` | Builds the command line from the WATO rule. |
| `src/aws_lambda_cw/rulesets/agent.py` | WATO form for the special agent (credentials, region, filter). |
| `src/aws_lambda_cw/rulesets/aws_lambda_cw.py` | WATO form for the check levels. |
| `src/aws_lambda_cw/agent_based/aws_lambda_cw.py` | Section parser, discovery and check function. |

## Configuration

Rule: **Setup → Agents → Other integrations → AWS Lambda (CloudWatch)**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `access_key_id` | String (required) | AWS access key ID. |
| `secret_key` | Password (required) | AWS secret access key. |
| `role_arn` | String (optional) | IAM role ARN to assume via `sts:AssumeRole` before reading CloudWatch. Use when the access key itself has no CloudWatch permissions and only serves to assume a (possibly cross-account) monitoring role. |
| `external_id` | String (optional) | `ExternalId` for `sts:AssumeRole`, only used together with `role_arn`. |
| `region` | String (required, default `eu-central-1`) | AWS region. |
| `functions` | List of strings (optional) | Limit to these function names; empty = auto-discover. |
| `interval` | Integer seconds (optional, default 600) | Metric look-back window. |

Rule: **Setup → Services → Service monitoring rules → AWS Lambda (CloudWatch)**
configures the upper levels for errors, error rate, throttles and duration.
