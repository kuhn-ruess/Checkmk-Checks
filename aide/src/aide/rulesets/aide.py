#!/usr/bin/env python3
"""
AIDE file integrity - check parameters

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    LevelDirection,
    ServiceState,
    SimpleLevels,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.form_specs.validators import NumberInRange
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "Evaluates the results of <tt>aide --check</tt> that <tt>cmk-aide-run</tt> "
            "stored on the host. Every difference to the AIDE database is CRIT by "
            "default: a legitimate change has to be reviewed and then either reverted "
            "or accepted by updating the AIDE database on the host "
            "(<tt>aide --update</tt>), after which the next run is OK again."
        ),
        elements={
            "state_changes": DictElement(
                parameter_form=ServiceState(
                    title=Title("State if AIDE reports differences"),
                    help_text=Help(
                        "Added, removed or changed entries compared to the AIDE database."
                    ),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
            ),
            "state_error": DictElement(
                parameter_form=ServiceState(
                    title=Title("State if the AIDE check fails"),
                    help_text=Help(
                        "AIDE could not run: missing or unreadable database or "
                        "configuration, timeout, aide not installed, or the result "
                        "file cannot be read by the agent."
                    ),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
            ),
            "state_missing": DictElement(
                parameter_form=ServiceState(
                    title=Title("State if there is no result yet"),
                    help_text=Help(
                        "The job is configured, but cmk-aide-run has never written a "
                        "result for it, for example because the timer is not active."
                    ),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
            ),
            "max_age": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Maximum age of the result"),
                    help_text=Help(
                        "A result older than this is outdated: the timer or the agent "
                        "plug-in stopped running AIDE. Set it to a multiple of the "
                        "interval of the timer. The age is measured with the clock of "
                        "the monitored host."
                    ),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=(
                            TimeMagnitude.DAY,
                            TimeMagnitude.HOUR,
                            TimeMagnitude.MINUTE,
                        ),
                    ),
                    prefill_fixed_levels=DefaultValue((10800.0, 21600.0)),
                ),
            ),
            "max_entries": DictElement(
                parameter_form=Integer(
                    title=Title("Number of changed paths shown in the details"),
                    custom_validate=(NumberInRange(min_value=1),),
                    prefill=DefaultValue(20),
                ),
            ),
        },
    )


rule_spec_aide = CheckParameters(
    name="aide",
    title=Title("AIDE file integrity"),
    topic=Topic.OPERATING_SYSTEM,
    parameter_form=_parameter_form,
    condition=HostAndItemCondition(item_title=Title("AIDE job")),
)
