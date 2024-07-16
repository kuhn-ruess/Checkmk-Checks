#!/usr/bin/env python
#pylint: disable=undefined-variable, missing-docstring


def agent_quobyte_arguments(params, hostname, ipaddress):
    args = '%s %s %s' % (params['api_url'], params['username'], params['password'])
    return args

special_agent_info['quobyte'] = agent_quobyte_arguments

