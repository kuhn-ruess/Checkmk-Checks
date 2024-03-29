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

def _item_spec_alteon_memory():
    return TextInput(
            title=_("Memory for core"),
        )


def _parameter_valuespec_alteon_memory():
    return Dictionary(
        elements = [
            ("alteon_memory_tresholds",
                Dictionary(
                    elements = [
                        ("percentVirtual",
                        Tuple(
                            title = "Tresholds (warn/crit) for Alteon Virtual Memory",
                            help = _("The provided tresholds are used for Virtual memory. The service ist Warning/Critical if this value exceeds the treshold"),
                            elements = [
                                Percentage(title = "Warning at a virtual memory usage above % of session limit", default_value = 75.0),
                                Percentage(title = "Critical at a virtual memory usage above % of session limit", default_value = 90.0),
                            ])),
                        ("percentRss",
                        Tuple(
                            title = "Tresholds (warn/crit) for Alteon RSS Memory",
                            help = _("The provided tresholds are used for RSS memory. The service ist Warning/Critical if this value exceeds the treshold"),
                            elements = [
                                Percentage(title = "Warning at a RSS memory usage above % of session limit", default_value = 75.0),
                                Percentage(title = "Critical at a RSS memory usage above % of session limit", default_value = 90.0),
                            ])),
                        ("CurrentSP",
                        Tuple(
                            title = "Tresholds (warn/crit) for Alteon Current Memory usage per Core",
                            help = _("The provided tresholds are used for Total Memory usage per Core. The service ist Warning/Critical if the memory of one core exceeds the treshold"),
                            elements = [
                                Percentage(title = "Warning at a RSS memory usage above % of session limit", default_value = 75.0),
                                Percentage(title = "Critical at a RSS memory usage above % of session limit", default_value = 90.0),
                            ])),
                        ])
    )
])


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="alteon_memory",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_alteon_memory,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_alteon_memory,
        title=lambda: _("Alteon Memory"),
    )
)
