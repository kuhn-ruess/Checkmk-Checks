#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

import base64
import json

from cmk.server_side_calls.v1 import (
    ActiveCheckCommand,
    ActiveCheckConfig,
    noop_parser,
)


def auto_downtime_commands(params, host_config):
    """Build the command line of the active check."""
    rules = base64.b64encode(json.dumps(params["rules"]).encode("utf-8")).decode("ascii")
    args = [
        "--user", params["username"],
        "--secret-id", params["secret"],
        "--host-name", host_config.name,
        "--service-name", params["description"],
        "--rules", rules,
    ]
    if params.get("url"):
        args += ["--url", params["url"]]
    if not params["verify_ssl"]:
        args.append("--no-verify-ssl")
    yield ActiveCheckCommand(service_description=params["description"], command_arguments=args)


active_check_auto_downtime = ActiveCheckConfig(
    name="auto_downtime",
    parameter_parser=noop_parser,
    commands_function=auto_downtime_commands,
)
