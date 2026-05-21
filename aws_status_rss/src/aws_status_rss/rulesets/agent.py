#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

WATO ruleset for the AWS Status RSS special agent.
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    List,
    String,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange, Url, UrlProtocol
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _feed_form():
    return Dictionary(
        elements={
            "name": DictElement(
                parameter_form=String(
                    title=Title("Service name"),
                    help_text=Help("Human readable AWS service name, e.g. 'Amazon CloudFront'"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "url": DictElement(
                parameter_form=String(
                    title=Title("Feed URL"),
                    help_text=Help("RSS or Atom feed URL (e.g. https://status.aws.amazon.com/rss/cloudfront.rss)"),
                    custom_validate=(Url(protocols=[UrlProtocol.HTTP, UrlProtocol.HTTPS]),),
                ),
                required=True,
            ),
        },
    )


def _form_special_agent_aws_status_rss():
    return Dictionary(
        title=Title("AWS service status RSS feeds"),
        help_text=Help(
            "Monitor the per-service status RSS/Atom feeds published by "
            "AWS at https://status.aws.amazon.com/. The agent fetches each "
            "configured feed and reports reachability plus the age of the "
            "most recent event."
        ),
        elements={
            "feeds": DictElement(
                parameter_form=List(
                    title=Title("Service feeds"),
                    element_template=_feed_form(),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "timeout": DictElement(
                parameter_form=Float(
                    title=Title("HTTP timeout"),
                    help_text=Help("Per-feed HTTP timeout in seconds."),
                    unit_symbol="s",
                    prefill=DefaultValue(15.0),
                ),
                required=False,
            ),
        },
    )


rule_spec_aws_status_rss = SpecialAgent(
    name="aws_status_rss",
    topic=Topic.CLOUD,
    parameter_form=_form_special_agent_aws_status_rss,
    title=Title("AWS service status RSS"),
)
