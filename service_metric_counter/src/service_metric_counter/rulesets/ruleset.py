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
    SimpleLevels,
    Integer,
    LevelDirection,
    InputHint,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange

from cmk.rulesets.v1.rule_specs import (
        SpecialAgent,
        Topic,
        CheckParameters,
        HostAndItemCondition,
        Topic,
)



def _valuespec_special_agent_service_metric_counter():
    """
    Service Metric Counter Special Agent Konfiguration
    """

    return Dictionary(
        title = Title("Service counter"),
        help_text = Help("This rule activates special agent for service counting"),
        elements = {
            "service_filters": DictElement(
                parameter_form = List(
                    title = Title("Services"),
                    help_text = Help("Pair of service names and service output pattern for counting"),
                    custom_validate=(LengthInRange(min_value=1),),
                    element_template = Dictionary(
                        elements = {
                            "name": DictElement(
                                parameter_form = String(
                                    title = Title("Name/Pattern for Service"),
                                    help_text = Help("Service name like Check_MK Agent, ..."),
                                    custom_validate=(LengthInRange(min_value=1),),
                                ),
                                required = True,
                            ),
                            "metric": DictElement(
                                parameter_form = String(
                                    title = Title("Metric which should be counted"),
                                    help_text = Help("Metric name you will find with the Service Details"),
                                    custom_validate=(LengthInRange(min_value=1),),
                                ),
                                required = True,
                            ),
                        },
                    )
                ),
                required = True,
            ),
            "path": DictElement(
                parameter_form = String(
                    title = Title("Path to Checkmk Site"),
                    help_text = Help("This is needed to access the Web API of "\
                                     "the central site, even if plugin is running on remote site."\
                                     "Example: https://server/site/"),
                    custom_validate=(LengthInRange(min_value=1),),
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
    name = "service_metric_counter",
    topic = Topic.APPLICATIONS,
    parameter_form = _valuespec_special_agent_service_metric_counter,
    title = Title("Service Metric counter"),
)



def _parameter_metric_counter() -> Dictionary:
    return Dictionary(
            elements={
                "levels": DictElement(
                    parameter_form=SimpleLevels[int](
                        title=Title("Levels"),
                        form_spec_template=Integer(unit_symbol="Count"),
                        level_direction=LevelDirection.UPPER,
                        prefill_fixed_levels=InputHint(value=(0, 0)),
                    )
                ),
                'metric_label' : DictElement(
                    parameter_form=String(
                        title = Title("Metric Label")
                    ),
                ),
                'metric_name' : DictElement(
                    parameter_form=String(
                        title = Title("Metric Name")
                    ),
                ),
            }
        )

rule_spec_metric_counter = CheckParameters(
    name="service_metric_counter",
    topic=Topic.APPLICATIONS,
    condition=HostAndItemCondition(item_title=Title("Pattern")),
    parameter_form=_parameter_metric_counter,
    title=Title("Service Metric Count"),
)
