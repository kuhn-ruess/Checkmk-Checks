"""
Service Counter
"""
from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    ListOf,
    Tuple,
    TextInput
)

try:
    # Checkmk 2.2
    from cmk.gui.plugins.wato.datasource_programs import (
        RulespecGroupDatasourceProgramsApps,
    )
    from cmk.gui.plugins.wato import (
        HostRulespec,
        rulespec_registry,
    )
except ImportError:
    # Pre Checkmk 2.2
    from cmk.gui.wato import RulespecGroupDatasourceProgramsApps
    from cmk.gui.watolib.rulespecs  import HostRulespec, rulespec_registry


def _valuespec_special_agents_service_counter():
    """
    Service Counter Special Agent Konfiguration
    """

    return Dictionary(
        title = _("Count and Sum Services"),
        help = _("This rule set selects the special agent for Service Counter"),
        elements = [
            ("service_filters", ListOf(
                valuespec=Tuple(
                    elements=[
                        TextInput(
                            title="Name of Service",
                            allow_empty=False,
                        ),
                        TextInput(
                            title="Service Pattern",
                            allow_empty= False,
                        )
                    ],
                )

            )),
        ],
        optional_keys=[],
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourceProgramsApps,
        name="special_agents:service_counter",
        valuespec=_valuespec_special_agents_service_counter,
    )
)
