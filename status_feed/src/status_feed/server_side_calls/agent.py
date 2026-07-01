"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Special agent invocation for the status feed plugin.
"""
from typing import Any

from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    HostConfig,
    NoProxy,
    SpecialAgentCommand,
    SpecialAgentConfig,
    URLProxy,
)


class FeedEntry(BaseModel):
    name: str
    url: str


class ConfigParser(BaseModel):
    feeds: list[FeedEntry]
    timeout: float | None = None
    user_agent: str | None = None
    # The backend replaces the Proxy form spec value with a URLProxy / EnvProxy
    # / NoProxy surrogate before parsing; keep it opaque and dispatch on type.
    proxy: Any = None


def agent_arguments(params: ConfigParser, host_config: HostConfig):
    args: list[str] = []
    if params.timeout:
        args.extend(["--timeout", str(params.timeout)])
    if params.user_agent:
        args.extend(["--user-agent", params.user_agent])
    if isinstance(params.proxy, URLProxy):
        args.extend(["--proxy", params.proxy.url])
    elif isinstance(params.proxy, NoProxy):
        args.append("--no-proxy")
    for feed in params.feeds:
        args.extend(["--feed", f"{feed.name}={feed.url}"])
    yield SpecialAgentCommand(command_arguments=args)


special_agent_status_feed = SpecialAgentConfig(
    name="status_feed",
    parameter_parser=ConfigParser.model_validate,
    commands_function=agent_arguments,
)
