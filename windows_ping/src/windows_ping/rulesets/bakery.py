#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
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
    Integer,
    LevelDirection,
    List,
    Percentage,
    SimpleLevels,
    String,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange, MatchRegex, NumberInRange
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _target() -> Dictionary:
    return Dictionary(
        elements={
            "address": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("IP address or host name"),
                    custom_validate=(
                        LengthInRange(min_value=1),
                        MatchRegex(r"^[^\s'\"]+$"),
                    ),
                ),
            ),
            "name": DictElement(
                parameter_form=String(
                    title=Title("Display name"),
                    help_text=Help(
                        "Used in the service name <tt>Ping &lt;display name&gt;</tt>. "
                        "Without a display name the address is used."
                    ),
                    custom_validate=(MatchRegex(r'^[^"]*$'),),
                ),
            ),
        },
    )


def _agent_config_windows_ping() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "Deploys the agent plug-in <tt>windows_ping.ps1</tt> to Windows hosts. "
            "It pings all configured targets concurrently from the monitored host "
            "and creates one local service <tt>Ping &lt;name&gt;</tt> per target "
            "with round trip time and packet loss."
        ),
        elements={
            "deployment": DictElement(
                required=True,
                parameter_form=CascadingSingleChoice(
                    title=Title("Deployment type"),
                    elements=(
                        CascadingSingleChoiceElement(
                            name="sync",
                            title=Title("Deploy the plug-in and run it synchronously"),
                            parameter_form=FixedValue(value=None),
                        ),
                        CascadingSingleChoiceElement(
                            name="cached",
                            title=Title("Deploy the plug-in and run it asynchronously"),
                            parameter_form=TimeSpan(
                                displayed_magnitudes=(
                                    TimeMagnitude.HOUR,
                                    TimeMagnitude.MINUTE,
                                    TimeMagnitude.SECOND,
                                ),
                                prefill=DefaultValue(120.0),
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            name="do_not_deploy",
                            title=Title("Do not deploy the plug-in"),
                            parameter_form=FixedValue(value=None),
                        ),
                    ),
                    prefill=DefaultValue("sync"),
                ),
            ),
            "targets": DictElement(
                required=True,
                parameter_form=List(
                    title=Title("Targets"),
                    help_text=Help("Hosts to ping from the monitored Windows host."),
                    element_template=_target(),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
            ),
            "count": DictElement(
                parameter_form=Integer(
                    title=Title("Echo requests per target"),
                    help_text=Help(
                        "Number of echo requests sent to every target per agent run. "
                        "Packet loss levels only make sense with more than one request."
                    ),
                    prefill=DefaultValue(1),
                    custom_validate=(NumberInRange(min_value=1, max_value=20),),
                ),
            ),
            "timeout": DictElement(
                parameter_form=Integer(
                    title=Title("Timeout per echo request"),
                    unit_symbol="ms",
                    prefill=DefaultValue(1000),
                    custom_validate=(NumberInRange(min_value=100, max_value=10000),),
                ),
            ),
            "rta_levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels on average round trip time"),
                    form_spec_template=Float(unit_symbol="ms"),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((100.0, 500.0)),
                ),
            ),
            "loss_levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels on packet loss"),
                    help_text=Help("A target without any reply is always critical."),
                    form_spec_template=Percentage(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue((40.0, 80.0)),
                ),
            ),
        },
    )


rule_spec_windows_ping_bakery = AgentConfig(
    name="windows_ping",
    title=Title("Windows Ping"),
    topic=Topic.WINDOWS,
    parameter_form=_agent_config_windows_ping,
)
