# hp_proliant_fix

Drop-in override for the built-in `hp_proliant_da_cntlr` check.

## Problem

On HPE ProLiant **Gen11** systems managed via **iLO 6**, the controller table
(`cpqDaCntlrTable`, `.1.3.6.1.4.1.232.3.2.2.1.1`) contains a phantom /
placeholder row — typically at index `0` — whose condition, board status and
board condition cells are all `0`. The vendor MIB has no `0` enum value, so
this is not a real controller.

The shipped check discovers a service for that row but rejects all-zero rows at
check time, leaving **`HW Controller 0`** permanently `UNKNOWN`
("Controller not found in SNMP data").

## Fix

This package ships a fixed `hp_proliant_da_cntlr` plugin at the **same
namespace path** as the built-in one
(`cmk/plugins/hp_proliant/agent_based/hp_proliant_da_cntlr.py`, installed under
`local/`). Because it is the identical module name, Checkmk's plugin loader
resolves it to the single local file and cleanly **shadows** the shipped
version — no duplicate-name conflict (verified with `cmk-validate-plugins`).

> Note: shipping the same plugin under a *different* family in
> `cmk_addons/plugins/` does **not** work cleanly — the loader keys plugins by
> name, so a differently-located copy registers the same name twice and
> `cmk-validate-plugins` reports an "already defined" error (it only wins at
> runtime by load order). Hence the same-path approach.

The fixed plugin skips phantom (all-zero) rows already during discovery, so no
bogus service is created. Behaviour for real controllers is unchanged. The
check logic is self-contained (no imports from `cmk.plugins` internals).

## Permanent WARN on Gen11 / iLO 6

On Gen11 / iLO 6, healthy controllers frequently report
`cpqDaCntlrBoardCondition` = `other`, even though `cpqDaCntlrCondition` is `ok`
and `cpqDaCntlrBoardStatus` is `enabled`. The built-in check maps `other` to
**WARN**, so the `HW Controller` service is stuck on WARN forever.

This package adds a check parameter rule **"HP ProLiant RAID controller"**
(*Setup → Service monitoring rules*) that remaps the state reported for the
`other` value of each column independently:

- *State when Condition is 'other'* (default WARN)
- *State when Board-Condition is 'other'* (default WARN) — set to **OK** to
  clear the Gen11/iLO6 false WARN
- *State when Board-Status is 'other'* (default WARN)

All defaults are WARN, i.e. identical to the built-in check, so installing the
package changes nothing until a rule is created.

## Compatibility

Checkmk 2.5 (the built-in check uses the agent_based v2 API there).

## Remove when

The upstream check skips phantom rows itself.
