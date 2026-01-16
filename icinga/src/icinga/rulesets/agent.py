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
        }

    )

rule_spec_agent_icinga = SpecialAgent(
    topic=Topic.APPLICATIONS,
    name="icinga",
    title=Title("Icinga Connector"),
    parameter_form=_form_special_agents_icinga,
)