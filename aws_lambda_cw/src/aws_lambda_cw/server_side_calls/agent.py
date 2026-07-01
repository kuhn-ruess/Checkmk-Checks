"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de

Special agent invocation for the AWS Lambda CloudWatch plugin.
"""
from pydantic import BaseModel

from cmk.server_side_calls.v1 import HostConfig, Secret, SpecialAgentCommand, SpecialAgentConfig


class ConfigParser(BaseModel):
    access_key_id: str
    secret_key: Secret
    role_arn: str | None = None
    external_id: str | None = None
    region: str = "eu-central-1"
    functions: list[str] | None = None
    interval: int | None = None


def agent_arguments(params: ConfigParser, host_config: HostConfig):
    args: list[str | Secret] = [
        "--access-key-id", params.access_key_id,
        "--secret-key", params.secret_key.unsafe(),
        "--region", params.region,
    ]
    if params.role_arn:
        args.extend(["--role-arn", params.role_arn])
    if params.external_id:
        args.extend(["--external-id", params.external_id])
    if params.interval:
        args.extend(["--interval", str(params.interval)])
    for function in params.functions or []:
        args.extend(["--function", function])
    yield SpecialAgentCommand(command_arguments=args)


special_agent_aws_lambda_cw = SpecialAgentConfig(
    name="aws_lambda_cw",
    parameter_parser=ConfigParser.model_validate,
    commands_function=agent_arguments,
)
