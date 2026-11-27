#!/usr/bin/env python3
"""
Azure Extra firewall check parameters

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    InputHint,
    Integer,
    LevelDirection,
    Percentage,
    ServiceState,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _throughput_levels(title, direction):
    """Levels for the firewall throughput in Mbit/s."""
    return SimpleLevels(
        title=title,
        level_direction=direction,
        form_spec_template=Float(unit_symbol="Mbit/s"),
        prefill_fixed_levels=InputHint((0.0, 0.0)),
    )


def _metrics_form():
    """Parameters of the Azure Firewall Metrics service."""
    return Dictionary(
        help_text=Help(
            "Levels for the metrics the Azure Extra special agent reads from Azure Monitor "
            "for an Azure Firewall. Network rule hits are the hits within the last minute, "
            "throughput is the average of the last minute."
        ),
        elements={
            "firewall_health": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Lower levels for the firewall health"),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Percentage(),
                    prefill_fixed_levels=DefaultValue((90.0, 50.0)),
                ),
            ),
            "network_rule_hits": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels for network rule hits per minute"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(unit_symbol="hits/min"),
                    prefill_fixed_levels=InputHint((0, 0)),
                ),
            ),
            "throughput_upper": DictElement(
                parameter_form=_throughput_levels(
                    Title("Upper levels for the throughput"), LevelDirection.UPPER
                ),
            ),
            "throughput_lower": DictElement(
                parameter_form=_throughput_levels(
                    Title("Lower levels for the throughput"), LevelDirection.LOWER
                ),
            ),
        },
    )


rule_spec_azure_firewall_metrics = CheckParameters(
    name="azure_firewall_metrics",
    title=Title("Azure Extra: Firewall metrics"),
    topic=Topic.APPLICATIONS,
    parameter_form=_metrics_form,
    condition=HostAndItemCondition(item_title=Title("Firewall name")),
)


def _ipconfig_form():
    """Parameters of the Azure Firewall IP Config service."""
    return Dictionary(
        help_text=Help(
            "The private IP, the public IP address and the public IP resource of a firewall "
            "IP configuration are stored when the service is discovered. If one of them "
            "changes later, the service goes to the state configured here until the "
            "service is discovered again, which accepts the new addresses."
        ),
        elements={
            "state_changed": DictElement(
                parameter_form=ServiceState(
                    title=Title("State if an address has changed since the service discovery"),
                    prefill=DefaultValue(ServiceState.CRIT),
                ),
            ),
        },
    )


rule_spec_azure_firewall_ipconfig = CheckParameters(
    name="azure_firewall_ipconfig",
    title=Title("Azure Extra: Firewall IP configuration"),
    topic=Topic.APPLICATIONS,
    parameter_form=_ipconfig_form,
    condition=HostAndItemCondition(item_title=Title("IP configuration")),
)
