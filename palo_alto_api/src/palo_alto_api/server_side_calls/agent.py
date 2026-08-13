"""
Palo Alto XML API Special Agent - Server Side Calls

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from pydantic import BaseModel

from cmk.server_side_calls.v1 import HostConfig, Secret, SpecialAgentCommand, SpecialAgentConfig


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


class ConfigParser(BaseModel):
    """
    Config Parser
    """
    api_key: Secret
    address: str | None = None
    timeout: int = 30
    no_verify_ssl: bool = False
    proxy_url: str | None = None
    collect: list[str] | None = None
    fetch_ciphers: bool = True
    cert_include: str | None = None
    cert_exclude: str | None = None
    if_include: str | None = None
    if_exclude: str | None = None


def agent_arguments(params: ConfigParser, host_config: HostConfig):
    """
    Build Special Agent Command Line
    """
    address = params.address or host_config.primary_ip_config.address
    args: list[str | Secret] = [
        "--host", address,
        "--api-key", params.api_key.unsafe(),
        "--timeout", str(params.timeout),
    ]

    if params.no_verify_ssl:
        args.append("--no-verify-ssl")

    if params.proxy_url:
        args.extend(["--proxy-url", params.proxy_url])

    selected = params.collect if params.collect is not None else ALL_SECTIONS
    args.extend(["--collect", ",".join(selected)])

    if not params.fetch_ciphers:
        args.append("--no-ciphers")

    if params.cert_include:
        args.extend(["--cert-include", params.cert_include])

    if params.cert_exclude:
        args.extend(["--cert-exclude", params.cert_exclude])

    if params.if_include:
        args.extend(["--if-include", params.if_include])

    if params.if_exclude is not None:
        args.extend(["--if-exclude", params.if_exclude])

    yield SpecialAgentCommand(command_arguments=args)


special_agent_palo_alto_api = SpecialAgentConfig(
    name="palo_alto_api",
    parameter_parser=ConfigParser.model_validate,
    commands_function=agent_arguments,
)
