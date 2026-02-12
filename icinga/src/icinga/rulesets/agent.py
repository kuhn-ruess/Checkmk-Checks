#!/usr/bin/env python3
"""
Icinga Connector

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from collections.abc import Sequence
from cmk.rulesets.v1 import Title

from cmk.rulesets.v1.form_specs import (
    Dictionary,
    Password,
    String,
    DictElement,
    List,
    BooleanChoice,
)

from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic

def _form_special_agents_icinga() -> Dictionary:
    return Dictionary(
        title=Title("Icinga Connection"),
        elements={
            'host_name': DictElement(
                parameter_form=String(
                    title=Title("Hostname with Port")
                ),
                required=True,
            ),
            'username': DictElement(
                parameter_form=String(
                    title=Title("Username")
                ),
                required=True,
            ),
            'password': DictElement(
                parameter_form=Password(
                    title=Title("Password")
                ),
                required=True,
            ),
            'ssl_verify': DictElement(
                parameter_form=BooleanChoice(
                    title=Title("SSL Certificate Verification"),
                    label=Title("Verify SSL certificates")
                ),
                required=False,
            ),
        }

    )

rule_spec_agent_icinga = SpecialAgent(
    topic=Topic.APPLICATIONS,
    name="icinga",
    title=Title("Icinga Connector"),
    parameter_form=_form_special_agents_icinga,
)