#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.d
"""

from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)
from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import (
        RulespecGroupMonitoringAgentsAgentPlugins
)

from cmk.gui.valuespec import (
    Age,
    Dictionary,
    TextAscii,
    ListOf,
    DropdownChoice,
    Tuple,
)


def _valuespec_check_docker_bakery():
    return Dictionary(
        title = "Docker Agent Based (Linux)",
        help = "Hosts configured via this rule get the <tt>docker.py</tt> plugin",
        elements = [
            ( "activated",
                DropdownChoice(
                    title = "Activation",
                    choices = [
                        ( True, "Deploy docker plugin" ),
                        ( None, "Do not deploy docker plugin" ),
                    ]
                )
            ),
            ( "interval",
                Age(
                    title = "Interval for docker check",
                    display = ["days", "hours", "minutes"],
                    default_value = 120,
                )
            ),
            ( "timeout",
                Age(
                    title = "Connection timeout",
                    display = ["minutes", "seconds"],
                    default_value = 30,
                )
            ),
            ( "label_whitelist",
                ListOf(
                    TextAscii(title="Label"),
                    title="Label Whitelist",
                )
            ),
            ( "label_replacements",
                ListOf(
                    Tuple(
                        elements = [
                            TextAscii(title="Original Label"),
                            TextAscii(title="Rewritten Label"),
                        ],
                    ),
                    title = "Label rewriting",
                )
            ),
            ( "piggyback",
                DropdownChoice(
                    title = "Use service swarm name as piggyback hostname",
                    choices = [
                        ( True, "Use service swarm name as piggyback hostname" ),
                        ( None, "Do not use service swarm name as piggyback hostname" ),
                    ]
                )
            ),
        ],
    )


rulespec_registry.register(
    HostRulespec(
        name="agent_config:check_docker",
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        valuespec=_valuespec_check_docker_bakery,
    )
)
