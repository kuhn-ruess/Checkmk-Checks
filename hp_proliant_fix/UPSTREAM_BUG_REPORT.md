# Upstream bug report (draft): `hp_proliant_da_cntlr` discovers a phantom RAID controller on ProLiant Gen11 / iLO 6

> Draft for submission to Checkmk (GitHub issue / forum). The working fix is
> shipped in this directory as the `hp_proliant_fix` MKP; see `README.md`.

## Summary

On HPE ProLiant **Gen11** servers managed via **iLO 6**, the built-in
`hp_proliant_da_cntlr` ("HW Controller") check discovers a service for a
phantom / placeholder row in `cpqDaCntlrTable` and can then never resolve it.
The resulting service — typically **`HW Controller 0`** — stays permanently
**UNKNOWN** with *"Controller not found in SNMP data"*, while all real
controllers are monitored correctly.

The root cause is internal to the plugin: the **parse** function already marks
the phantom row as `None`, but the **discovery** function iterates the section
*keys* and creates a service for it anyway. It is therefore a discovery bug,
not an SNMP / device problem.

## Affected versions

- **Checkmk 2.5** — `agent_based` v2 plugin
  `cmk/plugins/hp_proliant/agent_based/hp_proliant_da_cntlr.py`
- **Checkmk 2.4** — same defect in the legacy variant
  `share/check_mk/checks/hp_proliant_da_cntlr`

(Reproduced on 2.5.0 raw and 2.4.0p19 enterprise.)

## Environment

- Server: HPE ProLiant DL385 Gen11
- Management: iLO 6
- Monitoring: Checkmk SNMP, built-in `hp_proliant_da_cntlr`

## Root cause (Checkmk 2.5)

`cpqDaCntlrTable` (`.1.3.6.1.4.1.232.3.2.2.1.1`) on Gen11 / iLO 6 contains a
placeholder row — observed at index `0` — whose condition, role, board-status
and board-condition cells are all `"0"`. The vendor MIB defines no `0` enum
value, so this is not a real controller.

The plugin's `from_line()` correctly recognises this and stores `None` for that
row:

```python
# ControllerData.from_line()
if "0" in (cond, role, b_status, b_cond):
    return None
```

So the parsed section is `{ "0": None, "23": ControllerData(...) }`.

But discovery iterates the **keys**, ignoring whether the value is `None`:

```python
def discovery_hp_proliant_da_cntlr(section: ParsedSection) -> DiscoveryResult:
    if section:
        yield from (Service(item=item) for item in section)   # <-- discovers "0" too
```

A service `HW Controller 0` is created. At check time the value is `None`, so:

```python
def check_hp_proliant_da_cntlr(item, section):
    if not (subsection := section.get(item)):
        yield Result(state=State.UNKNOWN, summary="Controller not found in SNMP data")
        return
```

→ permanent UNKNOWN.

## Reproduction

1. Monitor a ProLiant Gen11 host (iLO 6) whose `cpqDaCntlrTable` carries the
   all-zero placeholder row at index 0.
2. Run service discovery for the HP ProLiant SNMP check.
3. Observe a discovered service `HW Controller 0`.

### Expected

No service is discovered for the placeholder row (consistent with the parser
already treating it as absent).

### Actual

`HW Controller 0` is discovered and is permanently **UNKNOWN** —
*"Controller not found in SNMP data"*.

## Proposed fix

Make discovery agree with parsing — skip rows whose parsed value is `None`.

**2.5 (`agent_based` v2):**

```python
def discovery_hp_proliant_da_cntlr(section: ParsedSection) -> DiscoveryResult:
    yield from (Service(item=item) for item, data in section.items() if data is not None)
```

**2.4 (legacy check):** the legacy variant keeps raw lines and only rejects
all-zero rows at check time; filter them out in discovery as well, e.g.:

```python
def inventory_hp_proliant_da_cntlr(info):
    # cond=line[3], b_status=line[5], b_cond=line[6]
    return [(line[0], None) for line in info if "0" not in (line[3], line[5], line[6])]
```

Behaviour for real controllers is unchanged. Verified against the original SNMP
walk: the only difference is that the bogus `HW Controller 0` service
disappears.

## Notes

- Independent of this bug, real controllers may legitimately be `WARN` when HP
  reports a board condition of `other` ("The instrument agent does not
  recognize the status of the controller"); that is existing, correct
  behaviour.
- A drop-in workaround that shadows the built-in plugin (same namespace path,
  installed under `local/`) is published as the `hp_proliant_fix` MKP in this
  repository for users who need a fix before an upstream release.

---

*Prepared by Kuhn & Rueß GmbH — https://kuhn-ruess.de*
