#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

WATO ruleset for the status feed special agent.
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    List,
    Proxy,
    String,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange, Url, UrlProtocol
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _feed_form():
    return Dictionary(
        elements={
            "name": DictElement(
                parameter_form=String(
                    title=Title("Feed name"),
                    help_text=Help(
                        "Human readable name, used as the service item, "
                        "e.g. 'Amazon CloudFront' or 'Scrivito'."
                    ),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "url": DictElement(
                parameter_form=String(
                    title=Title("Feed URL"),
                    help_text=Help(
                        "RSS or Atom feed URL, e.g. "
                        "https://status.aws.amazon.com/rss/cloudfront.rss or "
                        "https://status.scrivito.com/incidents.atom"
                    ),
                    custom_validate=(Url(protocols=[UrlProtocol.HTTP, UrlProtocol.HTTPS]),),
                ),
                required=True,
            ),
        },
    )


def _form_special_agent_status_feed():
    return Dictionary(
        title=Title("Status RSS/Atom feeds"),
        help_text=Help(
            "Monitor status RSS/Atom feeds. Works with the per-service status "
            "feeds published by AWS at https://status.aws.amazon.com/ as well "
            "as Statuspage-style incident-history feeds such as "
            "https://status.scrivito.com/incidents.atom. The agent fetches each "
            "configured feed and reports reachability, the age of the most "
            "recent event and the detected incident state."
        ),
        elements={
            "feeds": DictElement(
                parameter_form=List(
                    title=Title("Feeds"),
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
            "user_agent": DictElement(
                parameter_form=String(
                    title=Title("User-Agent header"),
                    help_text=Help(
                        "User-Agent sent with each request. Some endpoints "
                        "reject the default; a browser-like value can help."
                    ),
                    prefill=DefaultValue("checkmk-status-feed/1.0"),
                ),
                required=False,
            ),
            "proxy": DictElement(
                parameter_form=Proxy(
                    title=Title("HTTP proxy"),
                    help_text=Help(
                        "Proxy used to reach the feed URLs. Leave unset to use "
                        "the proxy configured in the process environment, or "
                        "choose 'No proxy' to always connect directly."
                    ),
                ),
                required=False,
            ),
        },
    )


rule_spec_status_feed = SpecialAgent(
    name="status_feed",
    topic=Topic.CLOUD,
    parameter_form=_form_special_agent_status_feed,
    title=Title("Status RSS/Atom feeds"),
)
