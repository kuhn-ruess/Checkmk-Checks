#!/usr/bin/env python3
# Copyright (C) 2017  Frank Fegert (fra.nospam.nk@gmx.de)
# Migration to cmk.rulesets.v1 by Kuhn & Ruess GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
"""WATO ruleset for the Open-iSCSI session statistics check."""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic

# (key, title, unit) for every session statistics counter.
_SESSION_STATS_PARAMS = [
    ("txdata_octets", "Transmitted bytes", "Bytes/sec"),
    ("rxdata_octets", "Received bytes", "Bytes/sec"),
    ("digest_err", "Digest (CRC) errors", "PDUs/sec"),
    ("timeout_err", "Timeout errors", "PDUs/sec"),
    ("noptx_pdus", "Transmitted NOP commands", "PDUs/sec"),
    ("noprx_pdus", "Received NOP commands", "PDUs/sec"),
    ("scsicmd_pdus", "Transmitted SCSI command requests", "PDUs/sec"),
    ("scsirsp_pdus", "Received SCSI command responses", "PDUs/sec"),
    ("tmfcmd_pdus", "Transmitted task management function commands", "PDUs/sec"),
    ("tmfrsp_pdus", "Received task management function responses", "PDUs/sec"),
    ("login_pdus", "Transmitted login requests", "PDUs/sec"),
    ("logout_pdus", "Transmitted logout requests", "PDUs/sec"),
    ("logoutrsp_pdus", "Received logout responses", "PDUs/sec"),
    ("text_pdus", "Transmitted text PDUs", "PDUs/sec"),
    ("textrsp_pdus", "Received text PDUs", "PDUs/sec"),
    ("dataout_pdus", "Transmitted data PDUs", "PDUs/sec"),
    ("datain_pdus", "Received data PDUs", "PDUs/sec"),
    ("snack_pdus", "Transmitted single negative ACKs", "PDUs/sec"),
    ("r2t_pdus", "Received ready to transfer PDUs", "PDUs/sec"),
    ("rjt_pdus", "Received reject PDUs", "PDUs/sec"),
    ("async_pdus", "Received asynchronous messages", "PDUs/sec"),
]


def _make_elements() -> dict:
    elements = {}
    for key, title, unit in _SESSION_STATS_PARAMS:
        elements[key] = DictElement(
            parameter_form=SimpleLevels(
                title=Title("%s") % title,
                help_text=Help("Levels for %s (%s).") % (title.lower(), unit),
                form_spec_template=Integer(unit_symbol=unit),
                level_direction=LevelDirection.UPPER,
                prefill_fixed_levels=DefaultValue((0, 0)),
            ),
        )
    return elements


def _parameter_form() -> Dictionary:
    return Dictionary(
        help_text=Help("The levels for the Open-iSCSI session statistics values."),
        elements=_make_elements(),
    )


rule_spec_open_iscsi_session_stats = CheckParameters(
    name="open_iscsi_session_stats",
    title=Title("Open-iSCSI Session Statistics"),
    topic=Topic.STORAGE,
    parameter_form=_parameter_form,
    condition=HostAndItemCondition(
        item_title=Title("MAC address and target IQN")
    ),
)
