#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

import keyword

from cmk.rulesets.v1 import Help, Label, Title
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    String,
)
from cmk.rulesets.v1.form_specs.validators import EmailAddress
from cmk.rulesets.v1.rule_specs import (
    NotificationParameters,
    Topic,
)


def _mail_elements():
    """
    Elements of the built-in HTML mail notification

    The plug-in hands its parameters to the built-in mail plug-in unchanged, so
    the very same form is offered here. If Checkmk ever moves that form, only
    the mail specific part of this rule disappears - the LDAP part keeps
    working.

    Keys that are no Python identifier are dropped: the ruleset API rejects
    them. That currently affects the sender ("from"), which is offered below
    under a valid key and translated back by the notification script.
    """
    try:
        elements = dict(_built_in_mail_form_spec().elements)
    except Exception:  # pylint: disable=broad-except
        return {}

    return {
        key: element
        for key, element in elements.items()
        if key.isidentifier() and not keyword.iskeyword(key)
    }


def _built_in_mail_form_spec():
    """
    The form of the built-in mail notification, 2.4 and 2.5 style
    """
    # pylint: disable=import-outside-toplevel
    from cmk.gui.wato._notification_parameter import _mail

    if hasattr(_mail, "form_spec_mail"):
        # 2.5
        return _mail.form_spec_mail()
    # 2.4
    return _mail.NotificationParameterMail()._form_spec()  # pylint: disable=protected-access


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


def _ldap_elements():
    """
    How to turn a group given as recipient into an address
    """
    return {
        "ldap": DictElement(
            parameter_form=Dictionary(
                title=Title("Resolve LDAP groups"),
                help_text=Help(
                    "Recipients without an '@' are looked up as LDAP groups, using the "
                    "LDAP connections already configured under Setup > Users > LDAP "
                    "connections. The address stored at the group object is used as "
                    "recipient. Recipients that already are mail addresses are passed "
                    "through untouched, so groups and mailboxes can be mixed."
                ),
                elements={
                    "connection": DictElement(
                        parameter_form=String(
                            title=Title("LDAP connection"),
                            help_text=Help(
                                "ID of the LDAP connection to query. Leave empty to try "
                                "all enabled connections in the configured order."
                            ),
                        ),
                    ),
                    "mail_attribute": DictElement(
                        parameter_form=String(
                            title=Title("Mail attribute of the group"),
                            help_text=Help(
                                "Attribute of the group object holding the address, "
                                "'mail' for mail enabled Active Directory groups."
                            ),
                            prefill=DefaultValue("mail"),
                        ),
                    ),
                    "group_filter": DictElement(
                        parameter_form=String(
                            title=Title("Custom group filter"),
                            help_text=Help(
                                "LDAP filter used to find the group below the group DN "
                                "of the connection. The macro $GROUP$ is replaced by the "
                                "given recipient. Leave empty to match the common name "
                                "or the account name of the group."
                            ),
                        ),
                    ),
                    "member_attribute": DictElement(
                        parameter_form=String(
                            title=Title("Member attribute of the group"),
                            help_text=Help(
                                "Only needed if the group uses a member attribute other "
                                "than member, uniqueMember or memberUid."
                            ),
                        ),
                    ),
                    "expand_members": DictElement(
                        parameter_form=BooleanChoice(
                            title=Title("Fall back to the group members"),
                            label=Label(
                                "Use the addresses of the members if the group itself "
                                "has no address"
                            ),
                            help_text=Help(
                                "Groups that are not mail enabled carry no address of "
                                "their own. With this option the addresses of all group "
                                "members are collected instead."
                            ),
                            prefill=DefaultValue(False),
                        ),
                    ),
                },
            ),
            required=True,
        ),
    }


def _parameters_mail_ldap_group():
    return Dictionary(
        title=Title("HTML email with LDAP group recipients"),
        elements=_ldap_elements() | _sender_element() | _mail_elements(),
    )


rule_spec_mail_ldap_group = NotificationParameters(
    title=Title("HTML email with LDAP group recipients"),
    topic=Topic.NOTIFICATIONS,
    parameter_form=_parameters_mail_ldap_group,
    name="mail_ldap_group",
)
