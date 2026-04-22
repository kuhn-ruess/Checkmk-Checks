"""
ERA output channels (OID branch .105 = outChannTable).
State + encoder labels; perfdata for Bps and total bytes.
"""
from .utils import detect_era, era_state, parse_int
from cmk.agent_based.v2 import (
    SNMPTree,
    CheckPlugin,
    SNMPSection,
    Service,
    Result,
    State,
    check_levels,
    OIDEnd,
)


def parse_era_outchann(string_table):
    section = {}
    for entry in string_table[0]:
        oid_end, state, enc1, enc2, bps, total = entry
        state = (state or '').strip()
        if not state or state == 'n/a':
            continue
        label = (enc1 or '').strip() or f"Channel {oid_end}"
        item = f"{oid_end} {label}"
        section[item] = {
            'state': state,
            'enc1': enc1,
            'enc2': enc2,
            'bps': bps,
            'bytes': total,
        }
    return section


def discover_era_outchann(section):
    for item in section:
        yield Service(item=item)


def check_era_outchann(item, params, section):
    data = section.get(item)
    if not data:
        return
    params = params or {}

    yield Result(state=era_state(data['state']), summary=f"State: {data['state']}")

    enc2 = (data['enc2'] or '').strip()
    if enc2:
        yield Result(state=State.OK, summary=f"Encoder2: {enc2}")

    bps = parse_int(data['bps'])
    if bps is not None:
        yield from check_levels(
            bps,
            levels_upper=params.get('bps_upper', ('no_levels', None)),
            levels_lower=params.get('bps_lower', ('no_levels', None)),
            metric_name='era_outchann_bps',
            render_func=lambda v: f"{v:.0f} B/s",
            label='Throughput',
            boundaries=(0, None),
        )

    total = parse_int(data['bytes'])
    if total is not None:
        yield from check_levels(
            total,
            metric_name='era_outchann_bytes',
            render_func=lambda v: f"{v:.0f} B",
            label='Total bytes',
            boundaries=(0, None),
        )


snmp_section_era_outchann = SNMPSection(
    name="era_outchann",
    detect=detect_era,
    parse_function=parse_era_outchann,
    fetch=[
        SNMPTree(
            base='.1.3.6.1.4.1.11588.1.5.105.1',
            oids=[
                OIDEnd(),
                '2',   # outChannState
                '3',   # outChannEnc1
                '4',   # outChannEnc2
                '71',  # outChannBps
                '72',  # outChannBytes
            ],
        ),
    ],
)


check_plugin_era_outchann = CheckPlugin(
    name='era_outchann',
    service_name='ERA OutChann %s',
    discovery_function=discover_era_outchann,
    check_function=check_era_outchann,
    check_ruleset_name='era_outchann',
    check_default_parameters={},
)
