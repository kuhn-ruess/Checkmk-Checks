"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Special agent invocation for the AWS Status RSS plugin.
"""
from pydantic import BaseModel

from cmk.server_side_calls.v1 import HostConfig, SpecialAgentCommand, SpecialAgentConfig


class FeedEntry(BaseModel):
    name: str
    url: str


class ConfigParser(BaseModel):
    feeds: list[FeedEntry]
    timeout: float | None = None


def agent_arguments(params: ConfigParser, host_config: HostConfig):
    args: list[str] = []
    if params.timeout:
        args.extend(["--timeout", str(params.timeout)])
    for feed in params.feeds:
        args.extend(["--feed", f"{feed.name}={feed.url}"])
    yield SpecialAgentCommand(command_arguments=args)


special_agent_aws_status_rss = SpecialAgentConfig(
    name="aws_status_rss",
    parameter_parser=ConfigParser.model_validate,
    commands_function=agent_arguments,
)
