#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    String,
    DefaultValue,
    InputHint,
    Password,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange

from cmk.rulesets.v1.rule_specs import (
        SpecialAgent,
        Topic,
)


def _valuespec_special_agent_sap_cloud_alm():
    """
    Special Agent Konfiguration
    """

    return Dictionary(
        title = Title("SAP Cloud ALM"),
        help_text = Help("This rule activates a special agent for the Cloud Serivce"),
        elements = {
            "instance": DictElement(
                parameter_form = String(
                    title = Title("Instance Name"),
                    help_text = Help("Instance Name is part of the Domain you got from SAP"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "client_id": DictElement(
                parameter_form = String(
                    title = Title("Client ID"),
                    help_text = Help("oAuth Client ID"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "client_secret": DictElement(
                parameter_form = Password(
                    title = Title("Client Secret"),
                    help_text = Help("oAuth Client Secret"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "metric_filter": DictElement(
                parameter_form = String(
                    title = Title("Metric Filter"),
                    help_text = Help("Filter like serviceId%20eq%20'53d0eade-85dc-4863-bc20-528954f52a23'"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
        },
    )


rule_spec_sap_cloud_alm = SpecialAgent(
    name = "sap_cloud_alm",
    topic = Topic.APPLICATIONS,
    parameter_form = _valuespec_special_agent_sap_cloud_alm,
    title = Title("SAP Cloud Alm"),
)
