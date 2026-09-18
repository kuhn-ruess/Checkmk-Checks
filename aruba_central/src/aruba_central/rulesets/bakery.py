#!/usr/bin/env python3
"""
Aruba Central - agent plugin deployment

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
    InputHint,
    Password,
    String,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _run_as() -> Dictionary:
    return Dictionary(
        title=Title("Run the plug-in as another user"),
        help_text=Help(
            "cencli keeps its token and its configuration in the home directory of "
            "the user that set it up, so the plug-in has to run as that user. On "
            "Windows the agent logs the user on, which needs the password; the "
            "password is written to the baked agent package and to the agent "
            "configuration on the host, and it must not contain spaces. On Linux "
            "the plug-in calls cencli with <tt>su</tt> (agent running as root) or "
            "<tt>sudo</tt>, no password is used."
        ),
        elements={
            "user": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("User name"),
                    help_text=Help(
                        "On Windows a domain user can be given as <tt>DOMAIN\\user</tt>."
                    ),
                    custom_validate=(LengthInRange(min_value=1),),
                    prefill=InputHint("cencli"),
                ),
            ),
            "password": DictElement(
                parameter_form=Password(
                    title=Title("Password"),
                    help_text=Help(
                        "Only used on Windows, where the agent has to log the user on."
                    ),
                ),
            ),
        },
    )


def _agent_config_aruba_central() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "Deploys the agent plug-in <tt>aruba_central</tt>, which calls "
            "<tt>cencli show aps -v --json</tt> and turns the result into one "
            "piggyback section per access point. The Linux and the Windows "
            "variant produce the same sections, cencli has to be installed and "
            "configured for the user the plug-in runs as. The call takes about 30 "
            "seconds, so it should be deployed asynchronously."
        ),
        elements={
            "deployment": DictElement(
                required=True,
                parameter_form=CascadingSingleChoice(
                    title=Title("Deployment type"),
                    elements=(
                        CascadingSingleChoiceElement(
                            name="cached",
                            title=Title("Deploy the plug-in and run it asynchronously"),
                            parameter_form=TimeSpan(
                                title=Title("Cache age"),
                                help_text=Help(
                                    "The plug-in is only run again when the cached "
                                    "data is older than this."
                                ),
                                displayed_magnitudes=(
                                    TimeMagnitude.HOUR,
                                    TimeMagnitude.MINUTE,
                                ),
                                prefill=DefaultValue(900.0),
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            name="sync",
                            title=Title("Deploy the plug-in and run it synchronously"),
                            parameter_form=FixedValue(value=None),
                        ),
                        CascadingSingleChoiceElement(
                            name="do_not_deploy",
                            title=Title("Do not deploy the plug-in"),
                            parameter_form=FixedValue(value=None),
                        ),
                    ),
                    prefill=DefaultValue("cached"),
                ),
            ),
            "timeout": DictElement(
                parameter_form=TimeSpan(
                    title=Title("Maximum runtime"),
                    help_text=Help(
                        "cencli needs about 30 seconds for a few hundred access "
                        "points. The default timeout of the agent is shorter than "
                        "that on Windows, so keep this above the runtime of the call."
                    ),
                    displayed_magnitudes=(
                        TimeMagnitude.MINUTE,
                        TimeMagnitude.SECOND,
                    ),
                    prefill=DefaultValue(300.0),
                ),
            ),
            "cencli": DictElement(
                parameter_form=String(
                    title=Title("Path to cencli"),
                    help_text=Help(
                        "Used when cencli is not in the PATH of the user the "
                        "plug-in runs as."
                    ),
                    prefill=InputHint("cencli"),
                ),
            ),
            "run_as": DictElement(
                parameter_form=_run_as(),
            ),
        },
    )


rule_spec_aruba_central_bakery = AgentConfig(
    name="aruba_central",
    title=Title("Aruba Central access points (cencli)"),
    topic=Topic.NETWORKING,
    parameter_form=_agent_config_aruba_central,
)
