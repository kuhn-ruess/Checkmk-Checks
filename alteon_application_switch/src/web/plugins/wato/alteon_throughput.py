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
    TextInput,
    Percentage,
    Tuple,
)

def _item_spec_alteon_throughput():
    return TextInput(
            title=_("Item"),
        )


def _parameter_valuespec_alteon_throughput():
    return Dictionary(
        elements = [
            ("alteon_throughput_tresholds",
            Tuple(
                title = "Tresholds (warn/crit) for Alteon Throughput",
                help = _("The provided tresholds are used for the current throughput. The service ist Warning/Critical if the values exceeds the trehshold"),
                elements = [
                    Percentage(title = "Warning when current throughput above % of limit", default_value = 70.0),
                    Percentage(title = "Critical  when current throughput above % of limit", default_value = 80.0),
                ])),
        ])


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="alteon_throughput",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_alteon_throughput,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_alteon_throughput,
        title=lambda: _("Alteon Throughput"),
    )
)
