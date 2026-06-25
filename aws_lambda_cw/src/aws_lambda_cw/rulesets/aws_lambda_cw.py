#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Check parameters for the AWS Lambda CloudWatch check.
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    Integer,
    LevelDirection,
    SimpleLevels,
    String,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    return Dictionary(
        elements={
            "levels_errors": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels for errors (count in window)"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(unit_symbol="errors"),
                    prefill_fixed_levels=DefaultValue((1, 10)),
                ),
                required=False,
            ),
            "levels_error_rate": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels for error rate"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(unit_symbol="%"),
                    prefill_fixed_levels=DefaultValue((5.0, 25.0)),
                ),
                required=False,
            ),
            "levels_throttles": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels for throttles (count in window)"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(unit_symbol="throttles"),
                    prefill_fixed_levels=DefaultValue((1, 10)),
                ),
                required=False,
            ),
            "levels_duration_avg": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels for average duration"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.SECOND, TimeMagnitude.MILLISECOND],
                    ),
                    prefill_fixed_levels=DefaultValue((1.0, 5.0)),
                ),
                required=False,
            ),
            "levels_duration_max": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels for maximum duration"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.SECOND, TimeMagnitude.MILLISECOND],
                    ),
                    prefill_fixed_levels=DefaultValue((5.0, 15.0)),
                ),
                required=False,
            ),
        },
    )


rule_spec_aws_lambda_cw = CheckParameters(
    name="aws_lambda_cw",
    topic=Topic.CLOUD,
    condition=HostAndItemCondition(
        item_title=Title("Lambda function name"),
        item_form=String(),
    ),
    parameter_form=_parameter_form,
    title=Title("AWS Lambda (CloudWatch)"),
)
