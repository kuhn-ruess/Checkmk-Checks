from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.rule_specs import NotificationParameters, Topic

#@ TODO BK: Risky Path, check on CMK Updates
from cmk.gui.wato._notification_parameter._mail import form_spec_mail


rule_spec_df_mail = NotificationParameters(
    name="df_mail",
    title=Title("Filesystem DF Mail"),
    topic=Topic.NOTIFICATIONS,
    parameter_form=form_spec_mail,
)
