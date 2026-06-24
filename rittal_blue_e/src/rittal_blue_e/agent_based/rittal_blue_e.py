"""
Rittal Blue e+ cooling unit monitoring (CMC III / IoT Interface, SNMP).

The bundled Checkmk cmciii check classifies sensors via a fixed
`sensor_type()` table that does not recognise the Blue e+ naming scheme
("Internal Temperature", "Monitoring.Cooling.Status", ...), so Blue e+
cooling units connected to a CMC III / IoT Interface are never discovered.

This plugin reads the same CMC III variable table
(`.1.3.6.1.4.1.2606.7.4.2.2.1`), keeps only sub-devices of type
"Blue e+" (from the device table `.1.3.6.1.4.1.2606.7.4.1.2.1`) and
creates services for them:

  * rittal_blue_e        - overall unit health (all component statuses)
                           plus cooling capacity / EER / input power
  * rittal_blue_e_temp   - internal / ambient / external temperature
  * rittal_blue_e_fan    - internal / external fan and compressor

Status fields only carry the integer code (cmcIIIMsgStatus) on the IoT
Interface firmware - cmcIIIVarValueStr is empty - so the code is mapped
to text/state here from the RITTAL-CMC-III-MIB enumeration.
"""
import re

from cmk.agent_based.v2 import (
    CheckPlugin,
    DiscoveryResult,
    Metric,
    OIDEnd,
    Result,
    Service,
    SNMPSection,
    SNMPTree,
    State,
    startswith,
)

CMC_BASE = ".1.3.6.1.4.1.2606.7"
BLUE_E_TYPE = "Blue e+"

# cmcIIIMsgStatus enumeration (RITTAL-CMC-III-MIB) -> display text.
STATUS_TEXT = {
    1: "not available",
    2: "configuration changed",
    3: "error",
    4: "OK",
    5: "alarm",
    6: "high warning",
    7: "low alarm",
    8: "high alarm",
    9: "low warning",
    10: "off",
    11: "on",
    12: "open",
    13: "closed",
    14: "locked",
    15: "unlocked (remote)",
    16: "door open",
    17: "service",
    18: "standby",
    19: "busy",
    20: "no access",
    21: "lost",
    22: "detected",
    23: "low voltage",
    24: "probe open",
    25: "probe short",
    26: "calibration",
    27: "inactive",
    28: "active",
    29: "no power",
    30: "read only",
    31: "exchanged",
    32: "valve open",
    33: "warning",
    34: "remote",
}

# Default Checkmk state per status code. Overridable via the ruleset.
DEFAULT_STATUS_STATE = {
    1: State.OK,    # not available -> sensor not present
    2: State.WARN,  # configuration changed
    3: State.CRIT,  # error
    4: State.OK,    # OK
    5: State.CRIT,  # alarm
    6: State.WARN,  # high warning
    7: State.CRIT,  # low alarm
    8: State.CRIT,  # high alarm
    9: State.WARN,  # low warning
    10: State.OK,   # off
    11: State.OK,   # on
    12: State.WARN,  # open
    13: State.OK,   # closed
    14: State.OK,   # locked
    15: State.WARN,  # unlocked (remote)
    16: State.WARN,  # door open
    17: State.OK,   # service
    18: State.OK,   # standby
    19: State.WARN,  # busy
    20: State.CRIT,  # no access
    21: State.CRIT,  # lost
    22: State.OK,   # detected
    23: State.WARN,  # low voltage
    24: State.CRIT,  # probe open
    25: State.CRIT,  # probe short
    26: State.WARN,  # calibration
    27: State.OK,   # inactive
    28: State.OK,   # active
    29: State.CRIT,  # no power
    30: State.OK,   # read only
    31: State.WARN,  # exchanged
    32: State.OK,   # valve open
    33: State.WARN,  # warning
    34: State.OK,   # remote
}

# Data types from cmcIIIVarType.
_STATUS_TYPES = {"7", "8"}          # status, statusEnum
_STRING_TYPES = {"1", "38"}         # description, stringValue
_NOT_AVAIL = 1

_SCALE_RE = re.compile(r"scale\s*([*/])\s*(\d+)")


def _parse_value(vtype, unit, constraints, value_str, value_int):
    """Return a normalised dict for one CMC III variable."""
    if vtype in _STATUS_TYPES:
        try:
            code = int(value_int)
        except ValueError:
            code = 0
        return {"kind": "status", "code": code,
                "text": STATUS_TEXT.get(code, "status %d" % code)}

    if vtype in _STRING_TYPES:
        return {"kind": "str", "text": value_str}

    # Numeric. Scale is encoded in the constraint string, e.g. "scale /100".
    try:
        raw = int(value_int)
    except ValueError:
        return {"kind": "str", "text": value_str}

    value = float(raw)
    m = _SCALE_RE.search(constraints or "")
    if m:
        op, factor = m.group(1), int(m.group(2))
        if factor:
            value = value / factor if op == "/" else value * factor
    return {"kind": "num", "value": value, "unit": unit}


def parse_rittal_blue_e(string_table):
    dev_rows, var_rows = string_table

    devices = {}
    for oidend, dtype, dname in dev_rows:
        devices[oidend] = {
            "type": dtype.strip(),
            "name": dname.strip() or ("Device %s" % oidend),
        }

    section = {}
    for oidend, name, vtype, unit, constraints, value_str, value_int in var_rows:
        devidx = oidend.split(".", 1)[0]
        dev = devices.get(devidx)
        if not dev or dev["type"] != BLUE_E_TYPE:
            continue
        entry = section.setdefault(dev["name"], {"type": dev["type"], "vars": {}})
        entry["vars"][name] = _parse_value(
            vtype, unit.strip(), constraints, value_str, value_int
        )
    return section


snmp_section_rittal_blue_e = SNMPSection(
    name="rittal_blue_e",
    detect=startswith(".1.3.6.1.2.1.1.2.0", CMC_BASE),
    parse_function=parse_rittal_blue_e,
    fetch=[
        # Device table: index, type, name/alias.
        SNMPTree(base=f"{CMC_BASE}.4.1.2.1", oids=[OIDEnd(), "2", "3"]),
        # Variable table: index (dev.var), name, type, unit, constraints,
        # value string, value int.
        SNMPTree(
            base=f"{CMC_BASE}.4.2.2.1",
            oids=[OIDEnd(), "3", "4", "5", "8", "10", "11"],
        ),
    ],
)


# --- helpers shared by the check functions ------------------------------

def _num(variables, key):
    var = variables.get(key)
    if var and var["kind"] == "num":
        return var["value"]
    return None


def _status(variables, key):
    var = variables.get(key)
    if var and var["kind"] == "status":
        return var["code"], var["text"]
    return None


def _status_state(code, params):
    text = STATUS_TEXT.get(code, "")
    for entry in (params or {}).get("status_states", []):
        if entry.get("status") == text:
            return State(entry["state"])
    return DEFAULT_STATUS_STATE.get(code, State.UNKNOWN)


# --- main service: overall unit health ----------------------------------

_COMPONENTS = [
    ("Monitoring.Cooling.Status", "Cooling"),
    ("Monitoring.Internal Air Circuit.Status", "Internal Air Circuit"),
    ("Monitoring.External Air Circuit.Status", "External Air Circuit"),
    ("Monitoring.Internal Fan.Status", "Internal Fan"),
    ("Monitoring.External Fan.Status", "External Fan"),
    ("Monitoring.Compressor.Status", "Compressor"),
    ("Monitoring.EEV.Status", "EEV"),
    ("Monitoring.Filter.Status", "Filter"),
    ("Monitoring.Door.Status", "Door"),
    ("Monitoring.Electronics.Status", "Electronics"),
    ("Monitoring.Condensate.Status", "Condensate"),
    ("Monitoring.System Messages.Status", "System Messages"),
    ("Monitoring.Error List.Status", "Error List"),
    ("Internal Temperature.Status", "Internal Temperature"),
    ("Ambient Temperature.Status", "Ambient Temperature"),
]


def discover_rittal_blue_e(section) -> DiscoveryResult:
    for item in section:
        yield Service(item=item)


def check_rittal_blue_e(item, params, section):
    data = section.get(item)
    if data is None:
        return
    variables = data["vars"]

    states = []
    details = []
    for key, label in _COMPONENTS:
        status = _status(variables, key)
        if status is None:
            continue
        code, text = status
        if code == _NOT_AVAIL:
            continue
        state = _status_state(code, params)
        states.append(state)
        details.append(Result(state=state, notice=f"{label}: {text}"))

    n_total = len(states)
    n_ok = sum(1 for s in states if s == State.OK)
    overall = State.worst(*states) if states else State.OK
    summary = f"{n_ok}/{n_total} components OK"
    if overall != State.OK:
        bad = [d.summary for d, s in zip(details, states) if s != State.OK]
        summary += " (" + ", ".join(bad) + ")"
    yield Result(state=State.OK, summary=summary)
    yield from details

    # Performance metrics.
    power = _num(variables, "Monitoring.Input Power")
    if power is not None:
        yield Metric("power", power)
    capacity = _num(variables, "Monitoring.Cooling.Capacity")
    if capacity is not None:
        yield Metric("cooling_capacity", capacity)
    eer = _num(variables, "Monitoring.Cooling.EER")
    if eer is not None:
        yield Metric("cooling_eer", eer)


check_plugin_rittal_blue_e = CheckPlugin(
    name="rittal_blue_e",
    service_name="Blue e+ %s",
    discovery_function=discover_rittal_blue_e,
    check_function=check_rittal_blue_e,
    check_ruleset_name="rittal_blue_e",
    check_default_parameters={},
)


# --- temperature sensors ------------------------------------------------

_TEMPS = [
    ("Internal Temperature", "Internal"),
    ("Ambient Temperature", "Ambient"),
    ("External Temperature Sensor", "External"),
]


def _temp_sensors(section):
    """Yield (item, device_name, sensor_key) for connected temp sensors."""
    for dev, data in section.items():
        variables = data["vars"]
        for key, label in _TEMPS:
            if _num(variables, f"{key}.Value") is None:
                continue
            status = _status(variables, f"{key}.Status")
            if status and status[0] == _NOT_AVAIL:
                continue
            yield f"{dev} {label}", dev, key


def discover_rittal_blue_e_temp(section) -> DiscoveryResult:
    for item, _dev, _key in _temp_sensors(section):
        yield Service(item=item)


def check_rittal_blue_e_temp(item, params, section):
    for cand, dev, key in _temp_sensors(section):
        if cand != item:
            continue
        variables = section[dev]["vars"]
        value = _num(variables, f"{key}.Value")

        warn, crit = None, None
        levels = (params or {}).get("levels")
        if isinstance(levels, tuple) and levels[0] == "fixed":
            warn, crit = levels[1]
        else:
            warn = _num(variables, f"{key}.SetPtHighWarning")
            crit = _num(variables, f"{key}.SetPtHighAlarm")

        state = State.OK
        if crit is not None and value >= crit:
            state = State.CRIT
        elif warn is not None and value >= warn:
            state = State.WARN

        status = _status(variables, f"{key}.Status")
        summary = f"{value:.1f} °C"
        if status is not None:
            summary += f" ({status[1]})"
            state = State.worst(state, _status_state(status[0], params))

        yield Result(state=state, summary=summary)
        if warn is not None and crit is not None:
            yield Metric("temp", value, levels=(warn, crit))
        else:
            yield Metric("temp", value)
        return


check_plugin_rittal_blue_e_temp = CheckPlugin(
    name="rittal_blue_e_temp",
    service_name="Blue e+ Temperature %s",
    sections=["rittal_blue_e"],
    discovery_function=discover_rittal_blue_e_temp,
    check_function=check_rittal_blue_e_temp,
    check_ruleset_name="rittal_blue_e_temp",
    check_default_parameters={},
)


# --- fans and compressor ------------------------------------------------

_FANS = [
    ("Monitoring.Internal Fan", "Value", "Internal Fan"),
    ("Monitoring.External Fan", "Value", "External Fan"),
    ("Monitoring.Compressor", "Speed", "Compressor"),
]


def _fan_sensors(section):
    for dev, data in section.items():
        variables = data["vars"]
        for key, field, label in _FANS:
            if _num(variables, f"{key}.{field}") is None:
                continue
            status = _status(variables, f"{key}.Status")
            if status and status[0] == _NOT_AVAIL:
                continue
            yield f"{dev} {label}", dev, key, field


def discover_rittal_blue_e_fan(section) -> DiscoveryResult:
    for item, _dev, _key, _field in _fan_sensors(section):
        yield Service(item=item)


def check_rittal_blue_e_fan(item, params, section):
    for cand, dev, key, field in _fan_sensors(section):
        if cand != item:
            continue
        variables = section[dev]["vars"]
        value = _num(variables, f"{key}.{field}")
        status = _status(variables, f"{key}.Status")

        state = State.OK
        summary = f"{value:.0f} %"
        if status is not None:
            summary += f" ({status[1]})"
            state = _status_state(status[0], params)

        yield Result(state=state, summary=summary)
        yield Metric("fan_perc", value)
        return


check_plugin_rittal_blue_e_fan = CheckPlugin(
    name="rittal_blue_e_fan",
    service_name="Blue e+ %s",
    sections=["rittal_blue_e"],
    discovery_function=discover_rittal_blue_e_fan,
    check_function=check_rittal_blue_e_fan,
    check_default_parameters={},
)
