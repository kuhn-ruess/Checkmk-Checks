#!/usr/bin/env python3
"""
AIDE file integrity - agent plug-in deployment

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Label, Message, Title
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    FixedValue,
    Integer,
    List,
    String,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange, MatchRegex, NumberInRange
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _job() -> Dictionary:
    return Dictionary(
        elements={
            "name": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("Name"),
                    help_text=Help(
                        "Becomes the item of the service <tt>AIDE &lt;name&gt;</tt> and "
                        "the name of the result file. Letters, digits, dot, dash and "
                        "underscore only."
                    ),
                    custom_validate=(
                        MatchRegex(
                            r"^[A-Za-z0-9_.-]+$",
                            error_msg=Message("Only letters, digits, '.', '-' and '_'."),
                        ),
                    ),
                    prefill=DefaultValue("system"),
                ),
            ),
            "config": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("AIDE configuration file"),
                    help_text=Help(
                        "Passed to <tt>aide --config</tt>. The configuration defines the "
                        "directories, the attributes that are compared and the database. "
                        "The database has to be initialised on the host before "
                        "(<tt>aide --init</tt>)."
                    ),
                    custom_validate=(LengthInRange(min_value=1),),
                    prefill=DefaultValue("/etc/aide.conf"),
                ),
            ),
        },
    )


def _agent_config_aide() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "Monitors the file integrity checks of AIDE. The package deploys "
            "<tt>cmk-aide-run</tt>, which runs <tt>aide --check</tt> for every job and "
            "stores the result below the result directory, and the agent plug-in "
            "<tt>aide</tt>, which hands these results to Checkmk. One service "
            "<tt>AIDE &lt;name&gt;</tt> is created per job.<br>"
            "AIDE itself and its databases are not managed by this rule: install AIDE, "
            "write the AIDE configuration and initialise the database on the host "
            "before. <tt>aide --check</tt> needs root to read protected directories, "
            "so when AIDE is run by the agent plug-in, the agent has to run as root; the "
            "systemd timer always runs as root."
        ),
        elements={
            "deployment": DictElement(
                required=True,
                parameter_form=CascadingSingleChoice(
                    title=Title("How AIDE is run"),
                    elements=(
                        CascadingSingleChoiceElement(
                            name="timer",
                            title=Title("By a systemd timer, the agent only reads the result"),
                            parameter_form=Dictionary(
                                elements={
                                    "interval": DictElement(
                                        required=True,
                                        parameter_form=TimeSpan(
                                            title=Title("Interval"),
                                            help_text=Help(
                                                "Time between two AIDE runs. Keep the "
                                                "maximum age of the check parameters "
                                                "above it."
                                            ),
                                            displayed_magnitudes=(
                                                TimeMagnitude.DAY,
                                                TimeMagnitude.HOUR,
                                                TimeMagnitude.MINUTE,
                                            ),
                                            prefill=DefaultValue(3600.0),
                                        ),
                                    ),
                                },
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            name="inline",
                            title=Title("By the agent plug-in on every call"),
                            parameter_form=Dictionary(
                                help_text=Help(
                                    "Only for small AIDE configurations that finish in "
                                    "a few seconds. A long run delays the agent."
                                ),
                                elements={
                                    "cache_age": DictElement(
                                        parameter_form=TimeSpan(
                                            title=Title("Run asynchronously with this cache age"),
                                            displayed_magnitudes=(
                                                TimeMagnitude.HOUR,
                                                TimeMagnitude.MINUTE,
                                            ),
                                            prefill=DefaultValue(600.0),
                                        ),
                                    ),
                                },
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            name="do_not_deploy",
                            title=Title("Do not deploy the plug-in"),
                            parameter_form=FixedValue(value=None),
                        ),
                    ),
                    prefill=DefaultValue("timer"),
                ),
            ),
            "jobs": DictElement(
                required=True,
                parameter_form=List(
                    title=Title("AIDE jobs"),
                    help_text=Help(
                        "One job per AIDE configuration. Use several jobs to check "
                        "different sets of directories separately."
                    ),
                    element_template=_job(),
                    add_element_label=Label("Add job"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
            ),
            "timeout": DictElement(
                parameter_form=TimeSpan(
                    title=Title("Maximum runtime of one AIDE run"),
                    help_text=Help(
                        "cmk-aide-run stops AIDE after this time and the service "
                        "reports a timeout."
                    ),
                    displayed_magnitudes=(TimeMagnitude.HOUR, TimeMagnitude.MINUTE),
                    prefill=DefaultValue(600.0),
                ),
            ),
            "max_lines": DictElement(
                parameter_form=Integer(
                    title=Title("Maximum number of output lines kept per job"),
                    help_text=Help(
                        "Limits the size of the result file and of the agent output "
                        "when very many files changed. The counts of the summary are "
                        "always complete."
                    ),
                    custom_validate=(NumberInRange(min_value=50),),
                    prefill=DefaultValue(2000),
                ),
            ),
            "result_dir": DictElement(
                parameter_form=String(
                    title=Title("Result directory"),
                    custom_validate=(LengthInRange(min_value=1),),
                    prefill=DefaultValue("/var/lib/cmk-aide"),
                ),
            ),
        },
    )


rule_spec_aide_bakery = AgentConfig(
    name="aide",
    title=Title("AIDE file integrity (Linux)"),
    topic=Topic.OPERATING_SYSTEM,
    parameter_form=_agent_config_aide,
)
