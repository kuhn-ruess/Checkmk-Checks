#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Label, Title
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    String,
)
from cmk.rulesets.v1.rule_specs import (
    AgentConfig,
    Topic,
)


def _valuespec_agent_storcli2():
    return Dictionary(
        title = Title("LSI Raid Controller Status 2 (via StorCLI2)"),
        help_text = Help(
            "This plug-in collects information on the logical volumes and physical disks "
            "of LSI RAID controllers using the StorCLI2 utility. StorCLI2 must be installed "
            "on the target system for this plug-in to work."
        ),
        elements = {
            "activate": DictElement(
                parameter_form = BooleanChoice(
                    label = Label("Deploy plugin"),
                ),
                required = True,
            ),
            "path": DictElement(
                parameter_form = String(
                    title = Title("Path"),
                    help_text = Help("Specify the path to storCLI2.exe"),
                    prefill = DefaultValue("C:\Program Files\StorCLI2\storCLI2.exe"),
                ),
            ),
        },
    )


rule_spec_storcli2 = AgentConfig(
    title = Title("LSI Raid Controller Status 2 (via StorCLI2)"),
    topic = Topic.OPERATING_SYSTEM,
    parameter_form = _valuespec_agent_storcli2,
    name = "storcli2",
)
