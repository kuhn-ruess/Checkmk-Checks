"""
WATO Config
"""
from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    ListOf,
    TextAscii,
)
from cmk.gui.plugins.wato import (
    rulespec_registry,
)
from cmk.gui.watolib.rulespec_groups import (
    RulespecGroupEnforcedServicesNetworking
)

from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithoutItem,
)

def _parameter_valuespec_cisco_portsec():
    return Dictionary(
        title=_("Cisco Portsecurity Exceptions"),
        elements=[
            (
                "exceptions",
                ListOf(TextAscii(title="Interface Name"),
                       title="Do not check the following Interfaces",
                       help="Alias Names also match with startswith")
            ),
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="cisco_portsec",
        group=RulespecGroupEnforcedServicesNetworking,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_cisco_portsec,
        title=lambda: _("Cisco Portsecurity Status"),
    )
)
