#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from collections.abc import Sequence
from pydantic import BaseModel, Field

from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    HostConfig,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
)

class CMDBSyncerParams(BaseModel):
    """
    Param Model
    """
    api_url: str
    password: Secret
    timeout: str
    services: Sequence[str] = Field(default_factory=list)

def generate_cmdbsyncer_command(params: CMDBSyncerParams, host_config: HostConfig):
    """
    CMD Line generation
    """
    args: list[str | Secret] = [
        "--api_url", params.api_url,
        "--password", params.password.unsafe(),
        "--timeout", params.timeout,
        "--services", ";".join(params.services),
    ]
    yield SpecialAgentCommand(command_arguments=args)

special_agent_CMDBSyncer = SpecialAgentConfig(
    name = "cmdb_syncer",
    parameter_parser = CMDBSyncerParams.model_validate,
    commands_function = generate_cmdbsyncer_command,
)
