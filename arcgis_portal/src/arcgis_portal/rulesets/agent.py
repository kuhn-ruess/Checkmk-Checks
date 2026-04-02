#!/usr/bin/env python3

"""
ArcGIS Portal Special Agent Ruleset
"""

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    String,
    Password,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange

from cmk.rulesets.v1.rule_specs import (
    SpecialAgent,
    Topic,
)


def _valuespec_special_agent_arcgis_portal():
    """
    Special Agent Konfiguration fuer ArcGIS Portal
    """

    return Dictionary(
        title=Title("ArcGIS Portal"),
        help_text=Help("This rule activates a special agent for ArcGIS Portal monitoring"),
        elements={
            "username": DictElement(
                parameter_form=String(
                    title=Title("Username"),
                    help_text=Help("Portal username for generateToken authentication"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "password": DictElement(
                parameter_form=Password(
                    title=Title("Password"),
                    help_text=Help("Portal password for generateToken authentication"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "proxy_url": DictElement(
                parameter_form=String(
                    title=Title("Proxy URL"),
                    help_text=Help("Proxy server URL to use for HTTP(S) requests (e.g., http://proxy.example.com:8080)"),
                ),
                required=False,
            ),
        },
    )


rule_spec_arcgis_portal = SpecialAgent(
    name="arcgis_portal",
    topic=Topic.APPLICATIONS,
    parameter_form=_valuespec_special_agent_arcgis_portal,
    title=Title("ArcGIS Portal"),
)
