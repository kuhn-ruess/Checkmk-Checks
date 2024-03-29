#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)
from cmk.gui.valuespec import (
    Dictionary,
    DropdownChoice,
    TextInput,
    Tuple,
)

def _item_spec_alteon_vrrp_status():
    return TextInput(
            title=_("Item"),
        )


def _parameter_valuespec_alteon_vrrp_status():
    return Dictionary(
        elements = [
            ("inventory_alteon_vrrp_state",
            Tuple(
                title = "Desired State for Cluster Status in this context",
                help = _("The Virtual Interfaces must provide the configured state, otherwise the check is warning.  Configure the desired state of all Intances in WATO using regex. If the cluster is switched, change the WATO config accordingly."),
                elements = [
                    DropdownChoice(choices=[
                        (2, _('Master')),
                        (3, _('Backup')),
                        (4, _('Holdoff')),
                    ])
                ])),
        ])


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="alteon_global",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_alteon_vrrp_status,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_alteon_vrrp_status,
        title=lambda: _("Alteon VRRP Status"),
    )
)
