from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Password,
    TextInput,
    Integer,
    Filesize,
)
from cmk.gui.plugins.wato import (
    rulespec_registry,
    HostRulespec,
)
from cmk.gui.plugins.wato.datasource_programs import (
    RulespecGroupDatasourceProgramsHardware,
)

from cmk.gui.watolib.rulespec_groups import (
    RulespecGroupEnforcedServicesStorage,
)

from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithItem,
    CheckParameterRulespecWithoutItem,
)

from cmk.gui.plugins.wato.utils.simple_levels import SimpleLevels

def _valuespec_special_agents_quobyte():
    return Dictionary(
        title = _("Quobyte via WebAPI"),
        help = _("This rule set selects the special agent for Quobyte"),
        elements = [
            ("api_url", TextInput(title = _("API Url"), allow_empty = False)),
            ("username", TextInput(title = _("Username"), allow_empty = False)),
            ("password", Password(title = _("Password"), allow_empty = False)),
        ],
        optional_keys=[],
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourceProgramsHardware,
        name="special_agents:quobyte",
        valuespec=_valuespec_special_agents_quobyte,
    )
)

def _parameter_valuespec_quobyte_volumes():
    return Dictionary(
        title=_("Quobyte Volume Levels"),
        elements=[
            (
                "used_allocated_space_bytes",
                SimpleLevels(Filesize, title=_("Allocated Space"), default_levels=(65.0, 90.0)),
            ),
            (
                "used_logical_space_bytes",
                SimpleLevels(Filesize, title=_("Used Logical Space "), default_levels=(65.0, 90.0)),
            ),
            (
                "used_disk_space_bytes",
                SimpleLevels(Filesize, title=_("Used Disk Space"), default_levels=(65.0, 90.0)),
            ),
            (
                "file_count",
                SimpleLevels(Integer, title=_("Total Count of Files"), default_levels=(0, 0)),
            ),
            (
                "directory_count",
                SimpleLevels(Integer, title=_("Total Count of Directories"), default_levels=(0, 0)),
            ),
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="quobyte_volumes",
        group=RulespecGroupEnforcedServicesStorage,
        match_type="dict",
        item_spec=lambda: TextInput(title=_("Volume Name")),
        parameter_valuespec=_parameter_valuespec_quobyte_volumes,
        title=lambda: _("Quobyte Volumes"),
    )
)
