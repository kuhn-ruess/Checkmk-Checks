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
    List,
    String,
    TimeSpan,
    TimeMagnitude,
    DefaultValue,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _valuespec_special_agent_service_counter():
    """
    Service Counter Special Agent Konfiguration
    """

    return Dictionary(
        title = Title("Service counter"),
        help_text = Help("This rule activates special agent for service counting"),
        elements = {
            "service_filters": DictElement(
                parameter_form = List(
                    title = Title("Service Defition"),
                    help_text = Help("Pair of service names and service output pattern for counting"),
                    custom_validate=(LengthInRange(min_value=1),),
                    element_template = Dictionary(
                        elements = {
                            "name": DictElement(
                                parameter_form = String(
                                    title = Title("Service Description Filter"),
                                    help_text = Help("Exact Service name like Check_MK Agent, ..."),
                                    custom_validate=(LengthInRange(min_value=1),),
                                ),
                                required = False,
                            ),
                            "service_pattern": DictElement(
                                parameter_form = String(
                                    title = Title("Service output Filter"),
                                    help_text = Help("Pattern, which will be searched in agent output for counting"),
                                    custom_validate=(LengthInRange(min_value=1),),
                                ),
                                required = False,
                            ),
                            "host_label_pattern": DictElement(
                                parameter_form = String(
                                    title = Title("Host Label Filter"),
                                    help_text = Help("Comma Seperated list of host label (key:value). Every Label needs to be given"),
                                    custom_validate=(LengthInRange(min_value=1),),
                                ),
                                required = False,
                            ),
                            "host_label_pattern_negated": DictElement(
                                parameter_form = String(
                                    title = Title("Host Label Filter Negated"),
                                    help_text = Help("Comma Seperated list of host label (key:value) which are not allowed to exist"),
                                    custom_validate=(LengthInRange(min_value=1),),
                                ),
                                required = False,
                            ),
                            "host_name_pattern": DictElement(
                                parameter_form = String(
                                    title = Title("Hostname (Regex) Filter"),
                                    help_text = Help("Enter a Hostname or an Regex for the Condition"),
                                    custom_validate=(LengthInRange(min_value=1),),
                                ),
                                required = False,
                            ),
                            "site_name_pattern": DictElement(
                                parameter_form = String(
                                    title = Title("Site Name Filter"),
                                    help_text = Help("Pattern, which will be searched in agent output for counting"),
                                    custom_validate=(LengthInRange(min_value=1),),
                                ),
                                required = False,
                            ),
                        },
                    )
                ),
                required = True,
            ),
            "timeout": DictElement(
                parameter_form = TimeSpan(
                    title = Title("Timeout"),
                    displayed_magnitudes=[TimeMagnitude.MILLISECOND, TimeMagnitude.SECOND],
                    prefill = DefaultValue(2.5),
                ),
                required = True,
            ),
        },
    )


rule_spec_service_counter = SpecialAgent(
    name = "service_counter",
    topic = Topic.APPLICATIONS,
    parameter_form = _valuespec_special_agent_service_counter,
    title = Title("Service counter"),
)
