#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

WATO ruleset for the generic endpoint freshness special agent.
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    FixedValue,
    Float,
    List,
    String,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange, Url, UrlProtocol
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _source_form():
    return CascadingSingleChoice(
        title=Title("Where to read the age from"),
        elements=(
            CascadingSingleChoiceElement(
                name="age_header",
                title=Title("HTTP response header 'Age' (seconds)"),
                parameter_form=FixedValue(value=None),
            ),
            CascadingSingleChoiceElement(
                name="date_header",
                title=Title("HTTP response header containing a date"),
                parameter_form=String(
                    title=Title("Header name"),
                    help_text=Help(
                        "Name of the header containing an HTTP date "
                        "(e.g. Last-Modified, Date)."
                    ),
                    prefill=DefaultValue("Last-Modified"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
            ),
            CascadingSingleChoiceElement(
                name="json_path",
                title=Title("JSON body field (dotted path)"),
                parameter_form=String(
                    title=Title("Dotted path"),
                    help_text=Help(
                        "Dotted path into the decoded JSON body. The "
                        "value at that path is parsed as ISO 8601 / "
                        "RFC 2822 date or as a raw number of seconds. "
                        "Use [N] for list indices, e.g. items[0].updated_at."
                    ),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
            ),
        ),
        prefill=DefaultValue("age_header"),
    )


def _endpoint_form():
    return Dictionary(
        elements={
            "name": DictElement(
                parameter_form=String(
                    title=Title("Service name"),
                    help_text=Help("Used as item in the 'Endpoint age' service."),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "url": DictElement(
                parameter_form=String(
                    title=Title("URL"),
                    custom_validate=(Url(protocols=[UrlProtocol.HTTP, UrlProtocol.HTTPS]),),
                ),
                required=True,
            ),
            "source": DictElement(
                parameter_form=_source_form(),
                required=True,
            ),
            "timeout": DictElement(
                parameter_form=Float(
                    title=Title("HTTP timeout"),
                    unit_symbol="s",
                    prefill=DefaultValue(15.0),
                ),
                required=False,
            ),
            "extra_headers": DictElement(
                parameter_form=List(
                    title=Title("Additional request headers"),
                    help_text=Help(
                        "Headers sent with the request, formatted as "
                        "'Name: Value' (e.g. 'Authorization: Bearer ...')."
                    ),
                    element_template=String(),
                ),
                required=False,
            ),
        },
    )


def _form_special_agent_endpoint_age():
    return Dictionary(
        title=Title("Endpoint age (generic HTTP freshness)"),
        help_text=Help(
            "Monitor whether an HTTP endpoint is being kept fresh "
            "(e.g. that a cronjob is still updating a JSON document, "
            "or that a CloudFront edge is serving recent content). "
            "Multiple endpoints may be queried per host."
        ),
        elements={
            "endpoints": DictElement(
                parameter_form=List(
                    title=Title("Endpoints"),
                    element_template=_endpoint_form(),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
        },
    )


rule_spec_endpoint_age = SpecialAgent(
    name="endpoint_age",
    topic=Topic.GENERAL,
    parameter_form=_form_special_agent_endpoint_age,
    title=Title("Endpoint age (HTTP freshness)"),
)
