"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""
from cmk.agent_based.v2 import (
    SimpleSNMPSection,
    CheckPlugin,
    Service,
    SNMPTree,
    State,
    Metric,
    Result,
    get_rate,
    get_value_store,
    contains,
)

DETECT_SONICWALL = contains('.1.3.6.1.2.1.1.1.0', 'sonicwall')
SONICWALL_VPN_OIDS = [
    ".1.3.6.1.4.1.8741.1.3.2.1.1.1.14",
    ".1.3.6.1.4.1.8741.1.3.2.1.1.1.2",
    ".1.3.6.1.4.1.8741.1.3.2.1.1.1.9",
    ".1.3.6.1.4.1.8741.1.3.2.1.1.1.11",
]

snmp_section_sonicwall_vpn = SimpleSNMPSection(
    name="sonicwall_vpn",
    detect=DETECT_SONICWALL,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.8741.1.3.2.1.1.1",
        oids=["14", "2", "9", "11"],
    ),
    parse_function=lambda section: [
        {
            "vpn_name": entry[0],
            "ip": entry[1],
            "bytes_enc": int(entry[2]),
            "bytes_dec": int(entry[3]),
        }
        for entry in section
    ] if section else [],
)

def discover_sonicwall_vpn(section):
    for entry in section:
        yield Service(item=entry["vpn_name"])

def check_sonicwall_vpn(item, section):
    data = next((e for e in section if e["vpn_name"] == item), None)
    if not data:
        yield Result(state=State.UNKNOWN, summary=f"No VPN data for {item}")
        return
    now = time.time()

    encrypted_bytes=data["bytes_enc"]
    decrypted_bytes=data["bytes_dec"]

    bytes_enc_rate = get_rate(get_value_store(), "vpn.enc.%s" % item, now, encrypted_bytes)
    bytes_dec_rate = get_rate(get_value_store(), "vpn.dec.%s" % item, now, decrypted_bytes)

    yield Metric("sa_bytes_encrypted", bytes_enc_rate)
    yield Metric("sa_bytes_decrypted", bytes_dec_rate)

    yield Result(state=State.OK, summary=f"SA ({item}/{data.get('ip')}) active")

check_plugin_sonicwall_vpn = CheckPlugin(
    name="sonicwall_vpn",
    service_name="VPN - %s",
    discovery_function=discover_sonicwall_vpn,
    check_function=check_sonicwall_vpn,
)
