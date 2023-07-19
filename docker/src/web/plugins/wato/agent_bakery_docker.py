#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-


from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
   HostRulespec,
   rulespec_registry,
)
from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
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
        title = _("Docker (Linux)"),
        help = _("Hosts configured via this rule get the <tt>docker</tt> plugin"),
        elements = [
            ( "activated",
              DropdownChoice(
                  title = _("Activation"),
                  choices = [
                      ( True, _("Deploy docker plugin") ),
                      ( None, _("Do not deploy docker plugin") ),
                  ]
            )),
            ( "interval",
              Age(
                 title = _("Interval for docker check"),
                 display = [ "days", "hours", "minutes" ],
                 default_value = 120,
            )),
            ( "label_whitelist", ListOf(
                TextAscii(title=_("Label")),
                title=_("Label Whitelist"),
            )),
            ( "label_replacements", ListOf(
                Tuple(
                    elements=[
                        TextAscii(title=_("Original Label")),
                        TextAscii(title=_("Rewritten Label")),
                    ],
                ),
                title=_("Label rewriting"),
            )),
        ],
    )


rulespec_registry.register(
    HostRulespec(
        name="agent_config:check_docker",
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        valuespec=_valuespec_check_docker_bakery,
    )
)
