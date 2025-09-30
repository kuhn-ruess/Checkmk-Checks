# 2021 created by Sven Rueß, sritd.de


from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    List,
    DictElement,
    Dictionary,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic, String


def _formspec_cohesity_node_status():
    return Dictionary(
        elements = {
            'services': DictElement(
                parameter_form=List(
                    title=Title("Services to ignore"),
                    help_text=Help("Specify all services to ignore"),
                    element_template=String(),
                ),
                required=True,
            ),
        },
    )


rule_spec_cohesity_node_status = CheckParameters(
    name = "cohesity_node_status",
    topic = Topic.STORAGE,
    condition=HostAndItemCondition(
        item_title=Title("Node"),
        item_form=String(),
    ),
    parameter_form = _formspec_cohesity_node_status,
    title = Title("Cohesity node status ignored services"),
)

