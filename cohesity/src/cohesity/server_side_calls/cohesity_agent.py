#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#pylint: disable=undefined-variable, missing-docstring
# +-----------------------------------------------------------------+
# |                                                                 |
# |        (  ___ \     | \    /\|\     /||\     /|( (    /|        |
# |        | (   ) )    |  \  / /| )   ( || )   ( ||  \  ( |        |
# |        | (__/ /     |  (_/ / | |   | || (___) ||   \ | |        |
# |        |  __ (      |   _ (  | |   | ||  ___  || (\ \) |        |
# |        | (  \ \     |  ( \ \ | |   | || (   ) || | \   |        |
# |        | )___) )_   |  /  \ \| (___) || )   ( || )  \  |        |
# |        |/ \___/(_)  |_/    \/(_______)|/     \||/    )_)        |
# |                                                                 |
# | Copyright Bastian Kuhn 2021                mail@bastian-kuhn.de |
# +-----------------------------------------------------------------+
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# 2021 reworked by Sven Rueß, sritd.de

from cmk.server_side_calls.v1 import noop_parser, SpecialAgentConfig, SpecialAgentCommand


def _agent_cohesity_arguments(params, host_config):
    args = [
        host_config.primary_ip_config.address,
        params['user'],
        params['password'].unsafe(),
        params['domain'],
        params['verify_cert']
    ]
    yield SpecialAgentCommand(command_arguments=args)


special_agent_cohesity = SpecialAgentConfig(
    name="cohesity",
    parameter_parser=noop_parser,
    commands_function=_agent_cohesity_arguments
)

