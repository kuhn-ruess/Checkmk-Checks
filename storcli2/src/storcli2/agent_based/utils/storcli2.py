#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""


from cmk.agent_based.v2 import (
    AgentSection,
)

def parse_storcli2_list(string_table):
    data = {}
    error = False

    for line in string_table:
        if line[-1] == ":":
            continue

        elif "ERROR" in line[0] or error:
            if not error:
                data["ERROR"] = []

            data["ERROR"].append(" ".join(line))
            error = True

        else:
            if "=" in line:
                key, value = map(lambda e: e.strip(), " ".join(line).split("="))
                data[key] = value
            else:
                continue

    return data

def parse_storcli2_table(string_table):
    data = {}
    head = True
    start = False
    end = 0

    for line in string_table:
        if "---" in line[0]:
            start = True
            end += 1
            continue

        elif start and end<=2:
            if head:
                fields = line
                head = False
            else:
                values = line
                data[values[0]] = {}

                if "Size" in fields:
                    index = fields.index("Size")
                    size = " ".join([values[index], values[index+1]])
                    values.pop(index+1)
                    values.pop(index)
                    values.insert(index, size)

                if len(fields) != len(values):
                    if "LU/NS" in fields:
                        fields.remove("LU/NS")

                for count in range(1, len(fields)):
                    data[values[0]][fields[count]] = values[count]

    return data
