#!/usr/bin/env python
#pylint: disable=undefined-variable, missing-docstring


def agent_servicecounter_arguments(params, hostname, ipaddress):
    args = " ".join([f"'{x}|{y}'" for x, y in params['service_filters']])
    return args

special_agent_info['service_counter'] = agent_servicecounter_arguments
