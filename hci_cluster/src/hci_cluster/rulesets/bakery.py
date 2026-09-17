#!/usr/bin/env python3
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Label, Title
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    FixedValue,
    SingleChoice,
    SingleChoiceElement,
    String,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _agent_config_hci_cluster() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "The plug-in <tt>hci_cluster</tt> allows monitoring of cluster nodes, "
            "resources, storage pools and disks. The Windows host needs the "
            "failover cluster cmdlets and permission to query the cluster."
        ),
        elements={
            "deployment": DictElement(
                required=True,
                parameter_form=CascadingSingleChoice(
                    title=Title("Deployment type"),
                    elements=(
                        CascadingSingleChoiceElement(
                            name="sync",
                            title=Title("Deploy the plug-in and run it synchronously"),
                            parameter_form=FixedValue(value=None),
                        ),
                        CascadingSingleChoiceElement(
                            name="cached",
                            title=Title("Deploy the plug-in and run it asynchronously"),
                            parameter_form=TimeSpan(
                                displayed_magnitudes=(
                                    TimeMagnitude.HOUR,
                                    TimeMagnitude.MINUTE,
                                )
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            name="do_not_deploy",
                            title=Title("Do not deploy the plug-in"),
                            parameter_form=FixedValue(value=None),
                        ),
                    ),
                    prefill=DefaultValue("sync"),
                ),
            ),
            "domain": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("Domain"),
                    help_text=Help("Domain the cluster is queried in."),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
            ),
            "filter_type": DictElement(
                required=True,
                parameter_form=SingleChoice(
                    title=Title("Filter type"),
                    help_text=Help("Restrict the clusters the plug-in reports on."),
                    # The names have to be python identifiers, so "None" from
                    # the pre-2.1.0 rule is spelled "no_filter" here; the bakery
                    # plug-in translates it back for the PowerShell config.
                    elements=[
                        SingleChoiceElement(name="no_filter", title=Title("No filter")),
                        SingleChoiceElement(name="inclusion", title=Title("Inclusion filter")),
                        SingleChoiceElement(name="exclusion", title=Title("Exclusion filter")),
                    ],
                    prefill=DefaultValue("no_filter"),
                ),
            ),
            "filter_pattern": DictElement(
                parameter_form=String(
                    title=Title("Filter pattern"),
                    label=Label("Example: HCI"),
                    help_text=Help("Matched against the cluster name. Ignored without a filter type."),
                ),
            ),
        },
    )


rule_spec_hci_cluster_bakery = AgentConfig(
    name="hci_cluster",
    title=Title("HCI Cluster Monitoring (Windows)"),
    topic=Topic.WINDOWS,
    parameter_form=_agent_config_hci_cluster,
)
