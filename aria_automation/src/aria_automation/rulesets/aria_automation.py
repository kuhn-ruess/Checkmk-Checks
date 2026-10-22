#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.rulesets.v1 import Help, Label, Title
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    ServiceState,
    SingleChoice,
    SingleChoiceElement,
    String,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange, NetworkPort, NumberInRange
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    SpecialAgent,
    Topic,
)


def _parameter_form_special_agent():
    return Dictionary(
        title=Title("VMware Aria Automation cluster services"),
        help_text=Help(
            "Queries '/api/v1/services/cluster' on an Aria Automation node. Every node "
            "answers with the services of the whole cluster, so the agent picks the "
            "service instances of the queried node by its node name and creates them "
            "as services on this host. The cluster wide service states can be sent as "
            "piggyback data to a separate host (for example the host of the cluster "
            "address). Assign the rule to every node host."
        ),
        elements={
            "protocol": DictElement(
                parameter_form=SingleChoice(
                    title=Title("Protocol"),
                    elements=[
                        SingleChoiceElement(name="http", title=Title("HTTP")),
                        SingleChoiceElement(name="https", title=Title("HTTPS")),
                    ],
                    prefill=DefaultValue("http"),
                ),
                required=True,
            ),
            "port": DictElement(
                parameter_form=Integer(
                    title=Title("Port"),
                    prefill=DefaultValue(8008),
                    custom_validate=(NetworkPort(),),
                ),
                required=True,
            ),
            "address": DictElement(
                parameter_form=String(
                    title=Title("Address to query"),
                    help_text=Help(
                        "Host name or IP address used in the URL. Default is the IP "
                        "address of the host, or its host name if it has none."
                    ),
                    custom_validate=(LengthInRange(min_value=1),),
                    macro_support=True,
                ),
                required=False,
            ),
            "node_name": DictElement(
                parameter_form=String(
                    title=Title("Node name"),
                    help_text=Help(
                        "Name of this node as reported in 'nodeName' of the cluster "
                        "data. Default is the host name. The name is compared case "
                        "insensitive, first in full and then by its first label, so a "
                        "short host name matches a fully qualified node name."
                    ),
                    custom_validate=(LengthInRange(min_value=1),),
                    macro_support=True,
                ),
                required=False,
            ),
            "cluster_host": DictElement(
                parameter_form=String(
                    title=Title("Send cluster wide services to host"),
                    help_text=Help(
                        "Host name in Checkmk that receives the cluster wide service "
                        "states as piggyback data. Every node delivers this data, so "
                        "the cluster host stays monitored while one node is down. "
                        "Without this option the cluster wide services are created "
                        "on each node host."
                    ),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required=False,
            ),
            "verify_cert": DictElement(
                parameter_form=BooleanChoice(
                    title=Title("TLS certificate verification"),
                    label=Label("Verify the certificate (HTTPS only)"),
                    prefill=DefaultValue(True),
                ),
                required=False,
            ),
            "timeout": DictElement(
                parameter_form=Integer(
                    title=Title("Timeout"),
                    unit_symbol="s",
                    prefill=DefaultValue(30),
                    custom_validate=(NumberInRange(min_value=1),),
                ),
                required=False,
            ),
        },
    )


rule_spec_aria_automation = SpecialAgent(
    name="aria_automation",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_special_agent,
    title=Title("VMware Aria Automation cluster services"),
)


def _parameter_form_service():
    return Dictionary(
        title=Title("VMware Aria Automation node service"),
        elements={
            "missing_state": DictElement(
                parameter_form=ServiceState(
                    title=Title("State if the service has no instance on this node"),
                    help_text=Help(
                        "The service still exists in the cluster but no instance runs "
                        "on this node any more, for example after a single instance "
                        "service moved to another node."
                    ),
                    prefill=DefaultValue(ServiceState.WARN),
                ),
                required=False,
            ),
        },
    )


rule_spec_aria_automation_service = CheckParameters(
    name="aria_automation_service",
    title=Title("VMware Aria Automation node service"),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_service,
    condition=HostAndItemCondition(item_title=Title("Service name")),
)
