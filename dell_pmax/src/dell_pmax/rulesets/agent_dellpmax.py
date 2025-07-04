#!/usr/bin/env python
"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""




from cmk.rulesets.v1 import Title, Help, Label
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    String,
    Password,
)

from cmk.rulesets.v1.form_specs.validators import LengthInRange

from cmk.rulesets.v1.rule_specs import (
        SpecialAgent,
        Topic,
)


def _valuespec_special_agent_dell_powermax():
    return Dictionary(
            title = Title("Check state of EMC PMAX storage pools"),
            help_text = Help("This rule set selects the <tt>dellpmax</tt> agent "\
                             "and allows monitoring of EMC PMAX storage pools by"\
                             "calling the REST API endpoints. "\
                             "Make sure you have an existing user "\
                             "as monitoring role and read-only permissions."),
            elements = {
                "username": DictElement(
                    parameter_form = String(
                        title = Title("Username"),
                        help_text = Help("Username on the storage system."\
                                         "Read only permissions are sufficient."\
                                         "Role has to be monitoring."),
                        custom_validate=(LengthInRange(min_value=1),),
                    ),
                    required = True,
                ),
                "password": DictElement(
                    parameter_form = Password(
                        title = Title("Password"),
                        help_text = Help("Password for the user on your storage system."),
                    ),
                    required = True,
                ),

            }
        )

rule_spec_semu_agent = SpecialAgent(
    name = "agent_dellpmax",
    topic = Topic.STORAGE,
    parameter_form = _valuespec_special_agent_dell_powermax,
    title = Title("Dell Powermax"),
)
