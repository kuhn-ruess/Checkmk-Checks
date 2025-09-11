from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    FixedValue,
    TimeMagnitude,
    TimeSpan,
    InputHint,
    String,
)
from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _agent_config_wordpress_instances() -> Dictionary:
    return Dictionary(
        help_text=Help(
            "This will deploy the agent plug-in <tt>wordpress_instances</tt>. "
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
                    prefill=DefaultValue("cached"),
                ),
            ),
            "base_dir": DictElement(
                parameter_form=String(
                    title=Title("Wordpress Base dir"),
                    prefill=InputHint('/var/www/sites.d'),
                ),
            ),
            "search_string": DictElement(
                parameter_form=String(
                    title=Title("Search String"),
                    prefill=InputHint('deploy/current'),
                ),
            ),
        },
    )


rule_spec_passwort_age = AgentConfig(
    name="wordpress_instances",
    title=Title("Wordpress Monitoring (Linux)"), 
    topic=Topic.OPERATING_SYSTEM,
    parameter_form=_agent_config_wordpress_instances,
)