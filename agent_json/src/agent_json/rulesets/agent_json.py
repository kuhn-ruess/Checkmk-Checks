#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consuling and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    List,
    String,
    Password,
    SingleChoice,
    SingleChoiceElement,
    DefaultValue,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _migrate(value):
    """
    Move the legacy single-endpoint format (api_url/method/username/password
    on the top level) into the new list-of-endpoints format so existing rules
    keep working.
    """
    if "endpoints" in value:
        return value

    endpoint = {}
    for key in ("api_url", "method", "username", "password"):
        if key in value:
            endpoint[key] = value[key]

    return {"endpoints": [endpoint]} if endpoint else value


def _endpoint_form():
    return Dictionary(
        title = Title("Endpoint"),
        elements = {
            "api_url": DictElement(
                parameter_form = String(
                    title = Title("API URL"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "method": DictElement(
                parameter_form = SingleChoice(
                    title = Title("HTTP method"),
                    help_text = Help(
                        "HTTP method used to query the API endpoint. "
                        "Defaults to POST to stay compatible with existing rules; "
                        "select GET for endpoints that serve the JSON on GET."
                    ),
                    elements = [
                        SingleChoiceElement(name = "post", title = Title("POST")),
                        SingleChoiceElement(name = "get", title = Title("GET")),
                    ],
                    prefill = DefaultValue("post"),
                ),
                required = False,
            ),
            "username": DictElement(
                parameter_form = String(
                    title = Title("Username"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = False,
            ),
            "password": DictElement(
                parameter_form = Password(
                    title = Title("Password"),
                ),
                required = False,
            ),
        },
    )


def _parameter_form_special_agent_json():
    return Dictionary(
        title = Title("Agent JSON"),
        help_text = Help("This rule set selects the special agent who parses json"),
        migrate = _migrate,
        elements = {
            "endpoints": DictElement(
                parameter_form = List(
                    title = Title("Endpoints"),
                    help_text = Help(
                        "One or more API endpoints to query. Every endpoint is "
                        "fetched with its own credentials and HTTP method; all "
                        "returned checks are merged into a single local section."
                    ),
                    element_template = _endpoint_form(),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
        },
    )


rule_spec_agent_json = SpecialAgent(
    name = "json",
    topic = Topic.SERVER_HARDWARE,
    parameter_form = _parameter_form_special_agent_json,
    title = Title("Agent JSON"),
)
