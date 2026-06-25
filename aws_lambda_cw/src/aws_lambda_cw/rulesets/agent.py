#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

WATO ruleset for the AWS Lambda CloudWatch special agent.
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    List,
    Password,
    String,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _form_special_agent_aws_lambda_cw():
    return Dictionary(
        title=Title("AWS Lambda (CloudWatch)"),
        help_text=Help(
            "Monitor AWS Lambda functions via CloudWatch for Checkmk editions "
            "without the built-in AWS Lambda integration. Needs an access key "
            "with the IAM permissions cloudwatch:ListMetrics and "
            "cloudwatch:GetMetricData."
        ),
        elements={
            "access_key_id": DictElement(
                parameter_form=String(
                    title=Title("Access key ID"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "secret_key": DictElement(
                parameter_form=Password(title=Title("Secret access key")),
                required=True,
            ),
            "region": DictElement(
                parameter_form=String(
                    title=Title("Region"),
                    help_text=Help("AWS region the functions live in, e.g. eu-central-1."),
                    prefill=DefaultValue("eu-central-1"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=True,
            ),
            "functions": DictElement(
                parameter_form=List(
                    title=Title("Limit to these functions"),
                    help_text=Help(
                        "Restrict monitoring to these function names. If left "
                        "empty, all functions reporting CloudWatch metrics are "
                        "discovered automatically."
                    ),
                    element_template=String(),
                ),
                required=False,
            ),
            "interval": DictElement(
                parameter_form=Integer(
                    title=Title("Look-back window"),
                    help_text=Help(
                        "Window in seconds over which the metrics are "
                        "aggregated. Should be >= the check interval."
                    ),
                    unit_symbol="s",
                    prefill=DefaultValue(600),
                ),
                required=False,
            ),
        },
    )


rule_spec_aws_lambda_cw = SpecialAgent(
    name="aws_lambda_cw",
    topic=Topic.CLOUD,
    parameter_form=_form_special_agent_aws_lambda_cw,
    title=Title("AWS Lambda (CloudWatch)"),
)
