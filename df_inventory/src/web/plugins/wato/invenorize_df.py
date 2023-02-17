#!/usr/bin/env python3
from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    DropdownChoice,
)
from cmk.gui.plugins.wato import (
    rulespec_registry,
    HostRulespec,
)

from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import (
    RulespecGroupMonitoringAgentsAgentPlugins,
)



def _valuespec():
    return DropdownChoice(
        title = _("Invenorize Filesystem Data (Linux)"),
        help = _("The plugin <tt>invenorize_df</tt> adds Filesystem Inventory Data"),
        choices=[
            (True, _("Deploy plugin")),
            (False, _("Do not deploy")),
        ],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        name="agent_config:df_inventory",
        valuespec=_valuespec,
    ))
