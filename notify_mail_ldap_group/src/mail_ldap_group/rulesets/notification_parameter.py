#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

import keyword

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import DictElement, Dictionary, String
from cmk.rulesets.v1.form_specs.validators import EmailAddress
from cmk.rulesets.v1.rule_specs import (
    NotificationParameters,
    Topic,
)


def _built_in_mail_elements():
    """
    Elements of the built-in HTML mail notification

    The plug-in hands its parameters to the built-in mail plug-in unchanged, so
    the very same form is offered here instead of duplicating it. Keys that are
    no Python identifier are dropped - the ruleset API rejects them. That
    affects the sender ("from"), which is offered below under a valid key.
    """
    try:
        # pylint: disable=import-outside-toplevel
        from cmk.gui.wato._notification_parameter import _mail

        if hasattr(_mail, "form_spec_mail"):
            elements = _mail.form_spec_mail().elements  # 2.5
        else:
            elements = _mail.NotificationParameterMail()._form_spec().elements  # 2.4
    except Exception:  # pylint: disable=broad-except
        return {}

    return {
        key: element
        for key, element in elements.items()
        if key.isidentifier() and not keyword.iskeyword(key)
    }


def _sender_element():
    """
    Replacement for the built-in "from" element, which cannot keep its key
    """
    return {
        "sender": DictElement(
            parameter_form=Dictionary(
                title=Title('Custom sender ("From")'),
                elements={
                    "address": DictElement(
                        parameter_form=String(
                            title=Title("Email address"),
                            custom_validate=[EmailAddress()],
                        ),
                    ),
                    "display_name": DictElement(
                        parameter_form=String(
                            title=Title("Display name"),
                        ),
                    ),
                },
            ),
        ),
    }


def _parameters_mail_ldap_group():
    return Dictionary(
        title=Title("HTML email with LDAP group recipients"),
        elements=_sender_element() | _built_in_mail_elements(),
    )


rule_spec_mail_ldap_group = NotificationParameters(
    title=Title("HTML email with LDAP group recipients"),
    topic=Topic.NOTIFICATIONS,
    parameter_form=_parameters_mail_ldap_group,
    name="mail_ldap_group",
)
