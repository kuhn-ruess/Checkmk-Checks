"""
Palo Alto XML API Special Agent - Server Side Calls

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.server_side_calls.v1 import (
    HostConfig,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
    noop_parser,
)


ALL_SECTIONS = [
    "certificates",
    "ipsec",
    "ike",
    "system",
    "sessions",
    "cpu",
    "environment",
    "ha",
    "interfaces",
    "bgp",
    "ospf",
    "licenses",
]


def agent_arguments(params, host_config: HostConfig):
    """
    Build Special Agent Command Line
    """
    address = params.get("address") or host_config.primary_ip_config.address
    args: list[str | Secret] = [
        "--host", address,
        "--timeout", str(params.get("timeout", 30)),
    ]

    auth_method, auth = params["auth"]
    if auth_method == "credentials":
        args += [
            "--username", auth["username"],
            "--password", auth["password"].unsafe(),
        ]
    else:
        args += ["--api-key", auth["key"].unsafe()]

    if params.get("no_verify_ssl"):
        args.append("--no-verify-ssl")

    if params.get("proxy_url"):
        args += ["--proxy-url", params["proxy_url"]]

    selected = params.get("collect") or ALL_SECTIONS
    args += ["--collect", ",".join(selected)]

    if not params.get("fetch_ciphers", True):
        args.append("--no-ciphers")

    if params.get("cert_include"):
        args += ["--cert-include", params["cert_include"]]

    if params.get("cert_exclude"):
        args += ["--cert-exclude", params["cert_exclude"]]

    if params.get("if_include"):
        args += ["--if-include", params["if_include"]]

    if params.get("if_exclude") is not None:
        args += ["--if-exclude", params["if_exclude"]]

    yield SpecialAgentCommand(command_arguments=args)


special_agent_palo_alto_api = SpecialAgentConfig(
    name="palo_alto_api",
    parameter_parser=noop_parser,
    commands_function=agent_arguments,
)
