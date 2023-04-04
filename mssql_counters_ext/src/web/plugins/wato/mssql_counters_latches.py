#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)
from cmk.gui.valuespec import (
    TextInput,
    Dictionary,
    Tuple,
    Integer,
)

def _item_spec_mssql_counters_latches():
    return TextInput(
        title=_("Instance"),
    )


def _parameter_valuespec_mssql_counters_latches():
    return Dictionary(
        title="MSSQL Latches",
        elements=[
            ("LatchWaits",
                Tuple(
                    title="Latch waits per second",
                    elements=[
                        Float(title="Warning at", default_value=100),
                        Float(title="Critical at", default_value=200),
                    ],
                )),
            ("LatchWaitTime",
                Tuple(
                    title="Total latch wait time (ms)",
                    elements=[
                        Float(title="Warning at", default_value=200),
                        Float(title="Critical at", default_value=400),
                    ],
                )),
            ("LatchAverage",
                Tuple(
                    title="Average latch wait time (ms",
                    elements=[
                        Float(title="Warning at", default_value=20),
                        Float(title="Critical at", default_value=40),
                    ],
                )),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="mssql_counters_latches",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_mssql_counters_latches,
        parameter_valuespec=_parameter_valuespec_mssql_counters_latches,
        title=lambda: _("MSSQL Latches"),
    )
)
