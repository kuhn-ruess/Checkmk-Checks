from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
from cmk.gui.plugins.wato import rulespec_registry, HostRulespec

from cmk.gui.valuespec import Alternative, Dictionary, FixedValue, TextAscii, DropdownChoice



def _valuespec():
    return Alternative(
        title = "Filesystemmonitoring of CIFS_FS via Plugin (Linux)",
        help = "The agent plugin will be deployed",
        elements=[
            FixedValue(True,
                       title="Do deploy plugin",
                       totext="(enabled)"),
            FixedValue(None,
                       title="Do not deploy plugin",
                       totext="(disabled)"),
        ],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        name="agent_config:cifs_df",
        valuespec=_valuespec,
    ))
