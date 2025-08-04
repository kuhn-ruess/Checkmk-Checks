#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
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
# | Copyright Bastian Kuhn 2018                mail@bastian-kuhn.de |
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

# Example output from agent:
# <<<qemu>>>
# 4 i-4B9008BE running 2048 4.0 2.7
# 5 i-44F608B6 running 2048 0.0 0.7

from cmk.agent_based.v2 import AgentSection, CheckPlugin, Metric, Result, Service, State


def parse_qemu(string_table):
    return string_table


def qemu_fix_vmname(name):
    # Reason for this not clear yet
    if name.startswith("instance"):
        name.replace("instance", "i")
    return name


def discover_qemu(section):
    for line in section:
        if line[2] == "running":
            vm = qemu_fix_vmname(line[1])
            yield Service(item=vm)


def check_qemu(item, params, section):
    perfdata = []
    for line in section:
        vm = qemu_fix_vmname(line[1])
        if vm == item:
            status = line[2]
            assigned_mem = line[3]
            infotext = ["Status: %s, id: %s" % (status, line[0])]
            state = 2
            if status == "running":
                state = 0
                current_cpu = int(round(float(line[4])))
                infotext.append("CPU: %s%%" % (current_cpu))

                current_mem = int(round(float(line[5])))
                infotext.append("Memory: (assigned: %s MB, used: %s%%)" % (assigned_mem, current_mem))

                perfdata.append(("cpu_util", current_cpu))
                perfdata.append(("memory_usage", current_mem))

                if params:
                    cpu_state = State.OK
                    mem_state = State.OK
                    if params.get('cpu'):
                        cpu_warn, cpu_crit = params['cpu']
                        if current_cpu >= cpu_crit:
                            cpu_state = State.CRIT
                        elif current_cpu >= cpu_warn:
                            cpu_state = State.WARN

                    if params.get('mem'):
                        mem_warn, mem_crit = params['mem']
                        if current_mem >= mem_crit:
                            mem_state = State.CRIT
                        elif current_cpu >= mem_warn:
                            mem_state = State.WARN
                    state = State.worst(mem_state, cpu_state)

            yield Result(state=state, summary=", ".join(infotext))
            for p in perfdata:
                yield Metric(p[0], p[1])


agent_section_qemu = AgentSection(
    name = "qemu",
    parse_function = parse_qemu,
)


check_plugin_qemu = CheckPlugin(
    name = "qemu",
    service_name = "VM %s",
    discovery_function = discover_qemu,
    check_function = check_qemu,
    check_default_parameters = {"cpu": None, "mem": None},
    check_ruleset_name = "qemu",
)
