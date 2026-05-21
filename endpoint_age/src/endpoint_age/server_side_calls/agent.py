"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Special agent invocation for the generic endpoint freshness plugin.
"""
import json

from pydantic import BaseModel

from cmk.server_side_calls.v1 import HostConfig, SpecialAgentCommand, SpecialAgentConfig


class Endpoint(BaseModel):
    name: str
    url: str
    source: tuple[str, str | None]
    timeout: float | None = None
    extra_headers: list[str] | None = None


class ConfigParser(BaseModel):
    endpoints: list[Endpoint]


def _source_to_str(source):
    kind, value = source
    if kind == "age_header":
        return "age_header"
    if kind == "date_header":
        return f"date_header:{value or 'Last-Modified'}"
    if kind == "json_path":
        return f"json_path:{value or ''}"
    return kind


def agent_arguments(params: ConfigParser, host_config: HostConfig):
    args: list[str] = []
    for ep in params.endpoints:
        payload = {
            "name": ep.name,
            "url": ep.url,
            "source": _source_to_str(ep.source),
        }
        if ep.timeout:
            payload["timeout"] = ep.timeout
        if ep.extra_headers:
            payload["header"] = ep.extra_headers
        args.extend(["--endpoint", json.dumps(payload, sort_keys=True)])
    yield SpecialAgentCommand(command_arguments=args)


special_agent_endpoint_age = SpecialAgentConfig(
    name="endpoint_age",
    parameter_parser=ConfigParser.model_validate,
    commands_function=agent_arguments,
)
