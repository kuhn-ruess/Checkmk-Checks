#!/usr/bin/env python3

"""
Service Group States Special Agent Ruleset

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Label, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    Integer,
    List,
    MatchingScope,
    RegularExpression,
    String,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange, NumberInRange
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _valuespec_special_agent_servicegroup_states():
    """
    Special Agent Konfiguration fuer Service Group States
    """
    return Dictionary(
        title=Title("Checkmk service group states"),
        help_text=Help(
            "This rule activates a special agent which reads the state of Checkmk "
            "service groups from Livestatus. Every service group matching one of the "
            "configured patterns becomes its own service on the host this rule is "
            "assigned to. Assign it to a host which represents the Checkmk site, "
            "since the agent runs on the Checkmk server itself."
        ),
        elements={
            "patterns": DictElement(
                parameter_form=List(
                    title=Title("Service group patterns"),
                    help_text=Help(
                        "Regular expressions (infix match) which are evaluated against the "
                        "service group names. The patterns are pushed down to Livestatus, "
                        "so the number of patterns, not the number of service groups, "
                        "determines the query size. Use '.*' to monitor all service groups."
                    ),
                    element_template=RegularExpression(
                        predefined_help_text=MatchingScope.INFIX,
                        custom_validate=(LengthInRange(min_value=1),),
                    ),
                    add_element_label=Label("Add pattern"),
                    remove_element_label=Label("Remove pattern"),
                    no_element_label=Label("No pattern configured"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "staleness": DictElement(
                parameter_form=Float(
                    title=Title("Staleness factor"),
                    help_text=Help(
                        "A service counts as stale from this staleness factor on. "
                        "This is the same value as the global setting "
                        "'Staleness value to force assume stale' (default: 1.5)."
                    ),
                    prefill=DefaultValue(1.5),
                    custom_validate=(NumberInRange(min_value=0.1),),
                ),
                required=False,
            ),
            "sockets": DictElement(
                parameter_form=List(
                    title=Title("Livestatus sockets"),
                    help_text=Help(
                        "By default the local site socket ($OMD_ROOT/tmp/run/live) is used. "
                        "For a distributed setup you can list one socket per site, either as "
                        "a path or as 'tcp:&lt;host&gt;:&lt;port&gt;'. The results of all "
                        "sites are merged per service group."
                    ),
                    element_template=String(
                        custom_validate=(LengthInRange(min_value=1),),
                    ),
                    add_element_label=Label("Add socket"),
                    remove_element_label=Label("Remove socket"),
                    no_element_label=Label("Use the local site socket"),
                ),
                required=False,
            ),
            "timeout": DictElement(
                parameter_form=Integer(
                    title=Title("Livestatus timeout"),
                    help_text=Help("Socket timeout in seconds (default: 30)"),
                    unit_symbol="s",
                    prefill=DefaultValue(30),
                    custom_validate=(NumberInRange(min_value=1),),
                ),
                required=False,
            ),
        },
    )


rule_spec_servicegroup_states = SpecialAgent(
    name="servicegroup_states",
    topic=Topic.GENERAL,
    parameter_form=_valuespec_special_agent_servicegroup_states,
    title=Title("Checkmk service group states"),
)
