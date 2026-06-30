#!/usr/bin/env python3
# Copyright (C) 2026 Kuhn & Rueß GmbH - License: GNU General Public License v2
#
# Local override of the built-in ``hp_proliant_da_cntlr`` check.
#
# Problem (observed on HPE ProLiant Gen11 / iLO 6, e.g. DL385 Gen11):
# the controller table (cpqDaCntlrTable, .1.3.6.1.4.1.232.3.2.2.1.1) contains a
# phantom/placeholder row at index 0 whose condition / board-status /
# board-condition cells are all "0". The vendor MIB has no "0" enum value, so
# such a row is not a real controller.
#
# The shipped plugin discovers a service for *every* table row (including the
# phantom one) but rejects all-zero rows at check time, leaving the service
# "HW Controller 0" permanently UNKNOWN ("Controller not found in SNMP data").
#
# This override keeps the check logic and output identical to upstream but
# skips phantom (all-zero) rows already at discovery time, so no bogus service
# is created. It re-registers the section and check plugin under the original
# names and therefore shadows the built-in ones.
#
# Self-contained on purpose (no imports from cmk.plugins internals) so the
# package stays portable across patch levels.

from collections.abc import Mapping

from cmk.agent_based.v2 import (
    any_of,
    CheckPlugin,
    CheckResult,
    contains,
    DiscoveryResult,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPTree,
    State,
    StringTable,
)

_PRODUCT_NAME_OID = ".1.3.6.1.4.1.232.2.2.4.2.0"

DETECT = any_of(
    contains(_PRODUCT_NAME_OID, "proliant"),
    contains(_PRODUCT_NAME_OID, "storeeasy"),
    contains(_PRODUCT_NAME_OID, "synergy"),
)

# cpqDaCntlrCondition / cpqDaCntlrBoardCondition
_COND_MAP: Mapping[str, tuple[State, str]] = {
    "1": (State.WARN, "other"),
    "2": (State.OK, "ok"),
    "3": (State.WARN, "degraded"),
    "4": (State.CRIT, "failed"),
}

# cpqDaCntlrRole
_ROLE_MAP: Mapping[str, str] = {
    "1": "other",
    "2": "notDuplexed",
    "3": "active",
    "4": "backup",
}

# cpqDaCntlrBoardStatus
_STATE_MAP: Mapping[str, tuple[State, str]] = {
    "1": (State.WARN, "other"),
    "2": (State.OK, "ok"),
    "3": (State.CRIT, "general failure"),
    "4": (State.CRIT, "cable problem"),
    "5": (State.CRIT, "powered off"),
    "6": (State.WARN, "cache module missing"),
    "7": (State.CRIT, "degraded"),
    "8": (State.OK, "enabled"),
    "9": (State.OK, "disabled"),
    "10": (State.CRIT, "standby (offline)"),
    "11": (State.OK, "standby (spare)"),
    "12": (State.WARN, "in test"),
    "13": (State.OK, "starting"),
    "14": (State.CRIT, "absent"),
    "16": (State.CRIT, "unavailable (offline)"),
    "17": (State.OK, "deferring"),
    "18": (State.OK, "quiesced"),
    "19": (State.WARN, "updating"),
    "20": (State.OK, "qualified"),
}

_OTHER_STATE_DESCRIPTION = (
    "The instrument agent does not recognize the status of the controller. "
    "You may need to upgrade the instrument agent."
)

Section = Mapping[str, list[str] | None]

# Default check parameters. All "other" states default to WARN, i.e. the exact
# behaviour of the built-in plugin. HPE ProLiant Gen11 / iLO 6 firmware tends to
# report cpqDaCntlrBoardCondition = other(1) for perfectly healthy controllers,
# which makes the service WARN forever; users can remap that here.
_DEFAULT_PARAMETERS = {
    "condition_other_state": 1,
    "board_condition_other_state": 1,
    "board_status_other_state": 1,
}


def _is_phantom(cond: str, role: str, b_status: str, b_cond: str) -> bool:
    """A real controller never reports the (non-existent) "0" enum value.

    Gen11 / iLO 6 exposes a placeholder row (typically at index 0) with all-zero
    cells; treat such rows as absent instead of monitoring them.
    """
    return "0" in (cond, role, b_status, b_cond)


def parse_hp_proliant_da_cntlr(string_table: StringTable) -> Section:
    section: dict[str, list[str] | None] = {}
    for line in string_table:
        _index, _model, _slot, cond, role, b_status, b_cond, _serial = line
        section[line[0]] = None if _is_phantom(cond, role, b_status, b_cond) else line
    return section


def discovery_hp_proliant_da_cntlr(section: Section) -> DiscoveryResult:
    yield from (Service(item=item) for item, line in section.items() if line is not None)


def _state_for(
    value: str, state_map: Mapping[str, tuple[State, str]], other_state: int
) -> tuple[State, str]:
    """Resolve a cell to (State, text); the "other"(1) state is configurable."""
    state, text = state_map[value]
    if value == "1":
        state = State(other_state)
    return state, text


def check_hp_proliant_da_cntlr(
    item: str, params: Mapping[str, int], section: Section
) -> CheckResult:
    line = section.get(item)
    if not line:
        yield Result(state=State.UNKNOWN, summary="Controller not found in SNMP data")
        return

    _index, model, slot, cond, role, b_status, b_cond, serial = line
    cond_state, cond_txt = _state_for(cond, _COND_MAP, params["condition_other_state"])
    bcond_state, bcond_txt = _state_for(b_cond, _COND_MAP, params["board_condition_other_state"])
    bstat_state, bstat_txt = _state_for(b_status, _STATE_MAP, params["board_status_other_state"])

    has_other = "1" in (cond, b_cond) or b_status == "1"
    yield Result(
        state=State.worst(cond_state, bcond_state, bstat_state),
        summary=(
            f"Condition: {cond_txt}, Board-Condition: {bcond_txt}, "
            f"Board-Status: {bstat_txt} "
            f"(Role: {_ROLE_MAP.get(role, 'unknown')}, Model: {model}, "
            f"Slot: {slot}, Serial: {serial})"
        ),
        details=_OTHER_STATE_DESCRIPTION if has_other else None,
    )


snmp_section_hp_proliant_da_cntlr = SimpleSNMPSection(
    name="hp_proliant_da_cntlr",
    detect=DETECT,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.232.3.2.2.1.1",
        oids=["1", "2", "5", "6", "9", "10", "12", "15"],
    ),
    parse_function=parse_hp_proliant_da_cntlr,
)

check_plugin_hp_proliant_da_cntlr = CheckPlugin(
    name="hp_proliant_da_cntlr",
    service_name="HW Controller %s",
    discovery_function=discovery_hp_proliant_da_cntlr,
    check_function=check_hp_proliant_da_cntlr,
    check_default_parameters=_DEFAULT_PARAMETERS,
    check_ruleset_name="hp_proliant_da_cntlr",
)
