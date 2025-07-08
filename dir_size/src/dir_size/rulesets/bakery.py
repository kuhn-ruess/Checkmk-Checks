
from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    List,
    DefaultValue,
    DictElement,
    Dictionary,
    FixedValue,
    Password,
    String,
    TimeMagnitude,
    TimeSpan,
    validators,
)
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _agent_config_dir_size() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "This will deploy the agent plug-in <tt>dir_size.sh</tt>. "
            "You can configure it to monitor directory sizes.."
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
            "folders": DictElement(
                required=True,
                parameter_form=List(
                    title=Title("Folder Paths"),
                    element_template=String(),

                )
            )
        },
    )


rule_spec_dir_size = AgentConfig(
    name="dir_size",
    title=Title("dir_size: Directory Size Monitoring"),
    topic=Topic.STORAGE,
    parameter_form=_agent_config_dir_size,
)
