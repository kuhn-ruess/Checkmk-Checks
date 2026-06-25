#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Check plugin: AWS Lambda metrics from CloudWatch.

One service per Lambda function. Reports invocations, errors (count and
rate), throttles and execution duration (average / maximum) over the
agent's look-back window, with configurable levels.
"""
import json

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    check_levels,
    render,
)


def parse_aws_lambda_cw(string_table):
    section = {}
    for row in string_table:
        if not row:
            continue
        try:
            entry = json.loads(row[0])
        except json.JSONDecodeError:
            continue
        name = entry.get("name")
        if not name:
            continue
        section[name] = entry
    return section


def discover_aws_lambda_cw(section):
    for name in section:
        yield Service(item=name)


def check_aws_lambda_cw(item, params, section):
    entry = section.get(item)
    if entry is None:
        return

    invocations = float(entry.get("invocations", 0.0))
    errors = float(entry.get("errors", 0.0))
    throttles = float(entry.get("throttles", 0.0))
    duration_avg = entry.get("duration_avg")
    duration_max = entry.get("duration_max")

    yield from check_levels(
        invocations,
        metric_name="aws_lambda_invocations",
        label="Invocations",
        render_func=lambda v: "%.0f" % v,
    )

    yield from check_levels(
        errors,
        levels_upper=params.get("levels_errors"),
        metric_name="aws_lambda_errors",
        label="Errors",
        render_func=lambda v: "%.0f" % v,
    )

    error_rate = (errors / invocations * 100.0) if invocations > 0 else 0.0
    yield from check_levels(
        error_rate,
        levels_upper=params.get("levels_error_rate"),
        metric_name="aws_lambda_error_rate",
        label="Error rate",
        render_func=render.percent,
    )

    yield from check_levels(
        throttles,
        levels_upper=params.get("levels_throttles"),
        metric_name="aws_lambda_throttles",
        label="Throttles",
        render_func=lambda v: "%.0f" % v,
    )

    if duration_avg is not None:
        yield from check_levels(
            float(duration_avg) / 1000.0,
            levels_upper=params.get("levels_duration_avg"),
            metric_name="aws_lambda_duration_avg",
            label="Duration (avg)",
            render_func=render.timespan,
        )
    if duration_max is not None:
        yield from check_levels(
            float(duration_max) / 1000.0,
            levels_upper=params.get("levels_duration_max"),
            metric_name="aws_lambda_duration_max",
            label="Duration (max)",
            render_func=render.timespan,
        )


agent_section_aws_lambda_cw = AgentSection(
    name="aws_lambda_cw",
    parse_function=parse_aws_lambda_cw,
)


check_plugin_aws_lambda_cw = CheckPlugin(
    name="aws_lambda_cw",
    service_name="AWS Lambda %s",
    discovery_function=discover_aws_lambda_cw,
    check_function=check_aws_lambda_cw,
    check_ruleset_name="aws_lambda_cw",
    check_default_parameters={
        "levels_errors": ("fixed", (1, 10)),
        "levels_throttles": ("fixed", (1, 10)),
    },
)
