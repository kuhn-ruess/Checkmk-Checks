#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.base.plugins.agent_based.agent_based_api.v1 import GetRateError

def get_docker_container_cpu(value_store, container):
    last_state = value_store.get("usage_counters")
    current_state = {
            "cpu_usage" : float(container["CPU_usage"]),
            "cpu_usage_system" : float(container["CPU_system_usage"]),
    }

    value_store["usage_counters"] = current_state
    if not last_state:
        raise GetRateError("Initialized usage counters")

    usage = current_state["cpu_usage"] - last_state["cpu_usage"]
    system_usage = current_state["cpu_usage_system"] - last_state["cpu_usage_system"]

    if usage < 0 or system_usage < 0:
        raise GetRateError("Value overflow")

    if system_usage == 0:
        raise GetRateError("No time difference")

    cpu_usage_percent = 100 * (usage / system_usage)
    return cpu_usage_percent
