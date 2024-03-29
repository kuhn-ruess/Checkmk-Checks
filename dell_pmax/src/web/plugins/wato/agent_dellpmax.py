#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------+
# |                                                            |
# |             | |             | |            | |             |
# |          ___| |__   ___  ___| | ___ __ ___ | | __          |
# |         / __| '_ \ / _ \/ __| |/ / '_ ` _ \| |/ /          |
# |        | (__| | | |  __/ (__|   <| | | | | |   <           |
# |         \___|_| |_|\___|\___|_|\_\_| |_| |_|_|\_\          |
# |                                   custom code by Nagarro   |
# |                                                            |
# +------------------------------------------------------------+
#
# Copyright (C)  2022  DevOps InfrastructureServices@nagarro-es.com
# for Nagarro ES GmbH

import cmk.gui.watolib as watolib
from cmk.gui.i18n import _
from cmk.gui.plugins.wato.datasource_programs import RulespecGroupDatasourcePrograms
from cmk.gui.plugins.wato import (
    rulespec_registry,
    HostRulespec,
)
from cmk.gui.valuespec import Password, TextAscii


def _valuespec_dellpmax():
    return Dictionary(
        elements=[
            (
                "username",
                TextAscii(
                    title=_("Username"),
                    help=_(
                        "Username on the storage system. Read only permissions are sufficient. Role has to be monitoring."
                    ),
                    allow_empty=False,
                ),
            ),
            (
                "password",
                Password(
                    title=_("Password"),
                    help=_("Password for the user on your storage system."),
                    allow_empty=False,
                    default_value="",
                ),
            ),
        ],
        optional_keys=False,
        title=_("Check state of EMC PMAX storage pools"),
        help=_(
            "This fucking rule set selects the <tt>dellpmax</tt> agent instead of the normal Check_MK Agent "
            "and allows monitoring of EMC PMAX storage pools by calling the REST API endpoints. "
            "Make sure you have an existing user as monitoring role and read-only permissions."
        ),
    )


rulespec_registry.register(
    (
        HostRulespec(
            group=RulespecGroupDatasourcePrograms,
            name="special_agents:dellpmax",
            valuespec=_valuespec_dellpmax,
        )
    )
)
