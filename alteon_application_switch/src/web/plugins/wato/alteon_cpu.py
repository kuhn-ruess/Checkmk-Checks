#!/usr/bin/env python3
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


def _item_spec_alteon_cpu():
    return TextInput(
            title=_("CPU Name"),
        )


def _parameter_valuespec_alteon_cpu():
    return Dictionary(
        elements = [
            ("alteon_cpu_utilization_tresholds",
            Tuple(
                title = "Tresholds (warn/crit) for Alteon CPU",
                help = _("The provided tresholds are used for Averages of 1, 4 and 64 seconds. The service ist Warning/Critical if one of these values exceeds the trehshold"),
                elements = [
                    Percentage(title = "Warning at a utilization of", default_value = 80, unit = _("%")),
                    Percentage(title = "Critical at a utilization of", default_value = 90, unit = _("%")),
                ])),
        ])


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="alteon_cpu",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_alteon_cpu,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_alteon_cpu,
        title=lambda: _("Alteon CPU"),
    )
)
