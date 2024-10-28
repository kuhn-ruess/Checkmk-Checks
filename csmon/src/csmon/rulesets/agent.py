#!/usr/bin/env python3
"""
CSMON Connector

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

def _form_special_agents_csmon() -> Dictionary:
    return Dictionary(
        title=Title("CSMON Connection"),
        elements={
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

rule_spec_agent_csmon = SpecialAgent(
    topic=Topic.APPLICATIONS,
    name="agent_csmon",
    title=Title("CSMON Connector"),
    parameter_form=_form_special_agents_csmon,
)
