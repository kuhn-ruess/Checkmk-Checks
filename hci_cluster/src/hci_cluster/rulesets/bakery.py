from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
from cmk.gui.plugins.wato import rulespec_registry, HostRulespec

from cmk.gui.valuespec import Alternative, Dictionary, FixedValue, TextAscii, DropdownChoice



def _valuespec():
    return Alternative(
        title = "HCI Cluster Monitoring (Windows)",
        help = "The plugin <tt>hci_cluster</tt> allows monitoring of Cluster Nodes, Resources, Storage Pools or Disks.",
        elements=[
            Dictionary(title="Deploy HCI Cluster plugin",
                       elements=[
                           ("domain", TextAscii(title="Domain", allow_empty=False)),
                           ("filter_type", DropdownChoice(title="Filter Type",
                                                          help="Exclusion or Inclusion",
                                                          choices=[
                                                            ("None", "No Filter"),
                                                            ("Inclusion", "Inclusion Filter"),
                                                            ("Exclusion", "Exclusion Filter"),
                                                          ],
                                                          default_value="None")),
                           ("filter_pattern", TextAscii(title="Filter Pattern",
                                                                help="Excample: HCI", allow_empty=True)),
                       ],
                       required_keys=["domain", "filter_type"]),
            FixedValue(None,
                       title="Do not deploy plugin",
                       totext="(disabled)"),
        ],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        name="agent_config:hci_cluster",
        valuespec=_valuespec,
    ))
