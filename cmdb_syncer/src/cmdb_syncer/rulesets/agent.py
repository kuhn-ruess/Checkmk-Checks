#!/usr/bin/env python3

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
    List,
    Password,
    DefaultValue,
    BooleanChoice,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _migrate(value):
    """
    Migration function to convert old parameter format to new format.
    Adds 'username' field if it doesn't exist.
    """
    if 'username' not in value:
        # Set default username to empty string when migrating old configurations
        value['username'] = ""
    return value


def _parameter_form_special_agents_cmdb_syncer():
    return Dictionary(
        title = Title("cmdb_syncer via WebAPI"),
        help_text = Help("This rule set selects the special agent for cmdb_syncer"),
        migrate = _migrate,
        elements = {
            "api_url": DictElement(
                parameter_form = String(
                    title = Title("API URL with http[s]://"),
                    custom_validate=(LengthInRange(min_value=1),),
                ),
                required = True,
            ),
            "username": DictElement(
                parameter_form = String(
                    title = Title("Username"),
                ),
                required = True,
            ),
            "password": DictElement(
                parameter_form = Password(
                    title = Title("Password")
                ),
                required = True,
            ),
            "timeout": DictElement(
                parameter_form = String(
                    title = Title("Timeout"),
                    prefill = DefaultValue(2.5),
                ),
                required = True,
            ),
            'services': DictElement(
                parameter_form=List(
                    title=Title("Services"),
                    element_template=String(),
                ),
                required=False,
            ),
            'fetch_cron': DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Fetch Cronjobs"),
                    label=Title("Fetch and Monitor Cronjobs"),
                ),
                required=False,
            ),
            'fetch_eda': DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Fetch Event Driven Ansible events"),
                    label=Label("Monitor events that are sent again and again without effect"),
                    help_text=Help(
                        "Creates the service <i>EDA Events</i> from the Syncer endpoint "
                        "<tt>syncer/eda</tt>. The API user needs the role <tt>syncer</tt> "
                        "(or <tt>all</tt>), like for the cronjobs. Syncer versions without "
                        "Event Driven Ansible answer 404, then no service is created."
                    ),
                ),
                required=False,
            ),
        },
    )


rule_spec_cmdb_syncer = SpecialAgent(
    name = "cmdb_syncer",
    topic = Topic.STORAGE,
    parameter_form = _parameter_form_special_agents_cmdb_syncer,
    title = Title("CMDB Syncer Monitoring"),
)
