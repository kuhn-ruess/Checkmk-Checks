from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
from cmk.gui.plugins.wato import rulespec_registry, HostRulespec

from cmk.gui.valuespec import Alternative, Dictionary, FixedValue, TextAscii



def _valuespec():
    return Alternative(
        title = _("HCI Cluster Monitoring (Windows)"),
        help = _("The plugin <tt>hci_cluster</tt> allows monitoring of Cluster Nodes, Resources, Storage Pools or Disks."),
        elements=[
            Dictionary(title=_("Deploy HCI Cluster plugin"),
                       elements=[
                           ("domain", TextAscii(title=_("Domain"), allow_empty=False)),
                           ("cluster_filter", TextAscii(title=_("Cluster Filter"), help="Use * as a Wildcard", allow_empty=False)),
                       ],
                       required_keys=["domain", "cluster_filter"]),
            FixedValue(None,
                       title=_("Do not deploy plugin"),
                       totext=_("(disabled)")),
        ],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        name="agent_config:hci_cluster",
        valuespec=_valuespec,
    ))
