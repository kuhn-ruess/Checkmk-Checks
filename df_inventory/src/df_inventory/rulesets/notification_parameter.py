from cmk.gui.watolib.notification_parameter import notification_parameter_registry, NotificationParameter

#@ TODO BK: Risky Path, check on CMK Updates
from cmk.gui.wato._notification_parameter import _mail as mail

from typing import cast
from cmk.gui.valuespec import Dictionary as ValueSpecDictionary
from cmk.gui.form_specs.vue.visitors.recomposers.unknown_form_spec import recompose

# This May work after 2.4
#class NotificationParameterDfMail(NotificationParameter):
#    """
#    Notification parameter for DF Mail
#    """
#    @property
#    def ident(self) -> str:
#        return "df_mail"
#
#    @property
#    def spec(self) -> ValueSpecDictionary:
#        # TODO needed because of mixed Form Spec and old style setup
#        return cast(ValueSpecDictionary, recompose(self._form_spec()).valuespec)
#
#    def _form_spec(self):
#        return mail.form_spec_mail

class NotificationParameterDfMail(mail.NotificationParameterMail):

    @property
    def ident(self) -> str:
        return "df_mail"


notification_parameter_registry.register(NotificationParameterDfMail)
