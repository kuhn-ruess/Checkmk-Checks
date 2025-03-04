#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.gui.cee.agent_bakery import RulespecGroupMonitoringAgentsAgentPlugins
from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    DropdownChoice
)
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry
)


def _valuespec_agent_lnx_sensors():
    return DropdownChoice(
        title = _("Sensors"),
        help = _("This will deploy the agent plugin <tt>lnx_sensors</tt> for monitoring the status of senores."),
        choices = [
            ( True, _("Deploy plugin for sensors") ),
            ( None, _("Do not deploy plugin for sensors") ),
        ]
    )


rulespec_registry.register(
    HostRulespec(
        name = "agent_config:lnx_sensors",
        group = RulespecGroupMonitoringAgentsAgentPlugins,
        valuespec = _valuespec_agent_lnx_sensors,
    )
)
