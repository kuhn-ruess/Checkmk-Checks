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

def _item_spec_alteon_sessions():
    return TextInput(
            title=_("Core"),
        )


def _parameter_valuespec_alteon_sessions():
    return Dictionary(
        elements = [
            ("alteon_session_tresholds",
            Tuple(
                title = "Tresholds (warn/crit) for Alteon Sessions per SP core",
                help = _("The provided tresholds are used for Averages of 1, 4 and 64 seconds. The service ist Warning/Critical if one of these values exceeds the trehshold"),
                elements = [
                    Percentage(title = "Warning at a session count above % of session limit", default_value = 80.0),
                    Percentage(title = "Critical at a session count above % of session limit", default_value = 90.0),
                ])),
            ("alteon_session_ssl_tresholds",
            Tuple(
                title = "Tresholds (warn/crit) for Alteon SSL Sessions",
                help = _("The provided tresholds are only used for Current SSL Sessions. The service ist Warning/Critical if this value exceeds the trehshold"),
                elements = [
                    Percentage(title = "Warning at a session count above % of session limit", default_value = 80.0),
                    Percentage(title = "Critical at a session count above % of session limit", default_value = 90.0),
                ])),
            ("alteon_slb_sessions_tresholds",
            Tuple(
                title = "Tresholds (warn/crit) for Alteon SLB Sessions",
                help = _("The provided tresholds are used for all Performance Values of SLB Sessions. The service ist Warning/Critical if one of this values exceeds the trehshold"),
                elements = [
                    Percentage(title = "Warning at a session count above % of session limit", default_value = 80.0),
                    Percentage(title = "Critical at a session count above % of session limit", default_value = 90.0),
                ])),
        ])


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="alteon_sessions",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_alteon_sessions,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_alteon_sessions,
        title=lambda: _("Alteon Sessions"),
    )
)
