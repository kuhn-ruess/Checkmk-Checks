#/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SINA L3 Monitoring
"""
__author__ = "Christian Michaelski"
__license__ = "GPL"
__version__ = "3.0.0"
__maintainer__ = "Christian Michaelski"
__email__ = "cmichaelski@conet.de"


"""
Updated 2025-05-23 for Checkmk 2.3/2.4 by Bastian Kuhn, bastian.kuhn@kuhn-ruess.de

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from cmk.agent_based.v2 import (
        CheckPlugin,
        Result,
        State,
        SNMPSection,
        SNMPTree,
        any_of,
        exists,
        Service,
        check_levels,
        Metric,
        get_value_store,
)
from cmk.plugins.lib.temperature import check_temperature

STATE = {
    0: "ERROR",
    1: "OK",
    2: "UNKNOWN"
}

HSB_MODE = {
    0: "INACTIVE",
    1: "ACTIVE",
    2: "STANDBY",
    3: "UNKNOWN"
}

WARN_TBL = {
   "601 - INVALID_EVENT": State.WARN,
   "602 - NOVUS_UPDATE_ERROR": State.CRIT,
   "603 - NOVUS_BAD_RECORD": State.WARN,
   "604 - NO_LDAP_CONFIGURED": State.OK,
   "605 - UPDATE_RECORDS_REMOVED": State.OK,
   "606 - SLOT_ERROR": State.CRIT,
   "607 - INSTALLATION_FAILED": State.CRIT,
   "608 - IMAGE_VERIFICATION_FAILED": State.WARN,
   "609 - DOWNLOAD_FAILED": State.WARN,
   "610 - RECORD_VERIFICATION_FAILED": State.WARN,
   "611 - UPDATES_VANISHED": State.OK,
   "612 - UPDATES_AVAILABLE": State.OK,
   "613 - DOWNLOAD_COMPLETE": State.OK,
   "614 - INSTALLATION_COMPLETE": State.OK,
   "615 - BLACKLISTED_ADMIN": State.WARN,
   "630 - SWITCH_SLOT_ERROR": State.CRIT,
   "642 - INTERNAL_ERROR": State.CRIT,
   "no error": State.OK,
   "": State.OK,
}

NSTATE = {
    0: "START",
    1: "INIT",
    2: "SYNC",
    3: "SKEW",
    4: "SYNC_LOST",
    5: "TIMEOUT",
    6: "NO_SYNC",
    7: "PARK",
    8: "BADCONF",
}

def parse_sinal3(string_table):
    parsed = {}
    if len(string_table[0]) != 0:
        parsed["temperature"] = string_table[0]
    if len(string_table[1]) != 0:
        parsed['fans'] = string_table[1]
    if len(string_table[2]) != 0:
        parsed['volts'] = string_table[2]
    if len(string_table[3]) != 0:
        parsed['system'] = string_table[3]
    if len(string_table[4]) != 0:
        parsed['mgmt'] = string_table[4]
    if len(string_table[5]) != 0:
        parsed['global'] = string_table[5]
    if len(string_table[6]) != 0:
        parsed['config'] = string_table[6]
    if len(string_table[7]) != 0:
        parsed['aclvers'] = string_table[7]
    if len(string_table[8]) != 0:
        parsed['vers'] = string_table[8][0][0]
        parsed['serial'] = string_table[8][0][1]
        parsed['box'] = string_table[8][0][2]
    if len(string_table[9]) != 0:
        parsed['ntp'] = string_table[9]
    if len(string_table[10]) != 0:
        parsed['policycnt'] = string_table[10]
    if len(string_table[11]) != 0:
        parsed['ipsec'] = string_table[11]
    if len(string_table[12]) != 0:
        parsed['ike-sa'] = string_table[12][0]
    return parsed

snmp_section_sinal3 = SNMPSection(
    name="sinal3",
    parse_function=parse_sinal3,
    fetch=[
        SNMPTree(
            # iso.org.dod.internet.private.enterprise.ucdavis.13.16.2.1.1 Nummer
            # iso.org.dod.internet.private.enterprise.ucdavis.13.16.2.2.1 Name
            # iso.org.dod.internet.private.enterprise.ucdavis.13.16.2.3.1 Temperatur
            base='.1.3.6.1.4.1.2021.13.16.2.1',
            oids=[
                '1', # sensor nr
                '2', # sensor name
                '3', # sensor temp 
            ],
        ),
        SNMPTree(
            # iso.org.dod.internet.private.enterprise.ucdavis.13.16.3.1.1 Nummer
            # iso.org.dod.internet.private.enterprise.ucdavis.13.16.3.2.1 Name
            # iso.org.dod.internet.private.enterprise.ucdavis.13.16.3.3.1 Drehzahl
            base='.1.3.6.1.4.1.2021.13.16.3.1',
            oids=[
                '1', # sensor nr
                '2', # sensor name
                '3', # sensor Drehzahl^ 
            ],
        ),
        SNMPTree(
            # iso.org.dod.internet.private.enterprise.ucdavis.13.16.4.1.1 Nummer
            # iso.org.dod.internet.private.enterprise.ucdavis.13.16.4.2.1 Name
            # iso.org.dod.internet.private.enterprise.ucdavis.13.16.4.3.1 Spannung
            base='.1.3.6.1.4.1.2021.13.16.4.1',
            oids=[
                '1', # sensor nr
                '2', # sensor name
                '3', # sensor volts 
            ],
        ),
        SNMPTree(
            # iso.org.dod.internet.private.enterprise.secunet.4.3.1.1 Software Version
            # iso.org.dod.internet.private.enterprise.secunet.4.3.1.8 HSB Mode
            # iso.org.dod.internet.private.enterprise.secunet.4.3.1.22 Zustand HS Verbindung
            # iso.org.dod.internet.private.enterprise.secunet.4.3.1.25 HSB mode
            # iso.org.dod.internet.private.enterprise.secunet.4.3.1.26 HSB mode partner
            base='.1.3.6.1.4.1.8299.4.3.1',
            oids=[
                '8', # HSB Mode
                '22', # zustand hsb verbindung
                '25', # hsb mode peer
                '26', # zustand hsb peer
            ],
        ),
        SNMPTree(
            # iso.org.dod.internet.private.enterprise.secunet.4.3.3.1 Version Main slot
            # iso.org.dod.internet.private.enterprise.secunet.4.3.3.2 Version Fallback slot
            # iso.org.dod.internet.private.enterprise.secunet.4.3.3.3 Verfügbare Software
            # iso.org.dod.internet.private.enterprise.secunet.4.3.3.5 SRSU Status
            # iso.org.dod.internet.private.enterprise.secunet.4.3.3.6 Letzte SRSU Meldung
            base='.1.3.6.1.4.1.8299.4.3.3',
            oids=[
                '1', # main slot
                '2', # fallback slot
                '3', # Verfügbare Version
                '5', # SRSU Status
                '6', # SRSU Meldung
            ],
        ),
        SNMPTree(
            # iso.org.dod.internet.private.enterprise.secunet.4.3.1.0 Globaler Status int
            # iso.org.dod.internet.private.enterprise.secunet.4.3.1.7 Globaler Status
            base='.1.3.6.1.4.1.8299.4.3.1',
            oids=[
                '6', # globaler status int
                '7', # globaler status
            ],
        ),
        SNMPTree(
            # iso.org.dod.internet.private.enterprise.secunet.4.3.3.7 Active
            # iso.org.dod.internet.private.enterprise.secunet.4.3.3.8 System-CFS
            # iso.org.dod.internet.private.enterprise.secunet.4.3.3.9 Smartcard
            base='.1.3.6.1.4.1.8299.4.3.3',
            oids=[
                '7', # active
                '8', # system-cfs
                '9', # Smartcard
            ],
        ),
        SNMPTree(
            # iso.org.dod.internet.private.enterprise.secunet.4.3.1.4 ACL active
            # iso.org.dod.internet.private.enterprise.secunet.4.3.1.5  ACL smartcard
            base='.1.3.6.1.4.1.8299.4.3.1',
            oids=[
                '4', # acl active
                '5', # acl smartcard
            ],
        ),
        SNMPTree(
            # iso.org.dod.internet.private.enterprise.secunet.4.3.1.1 running version
            # iso.org.dod.internet.private.enterprise.secunet.4.3.1.13 Serial
            # iso.org.dod.internet.private.enterprise.secunet.4.3.1.27 Box type
            base='.1.3.6.1.4.1.8299.4.3.1',
            oids=[
                '1', # running version
                '13', # serial
                '27', # box type
            ],
        ),
        SNMPTree(
            # iso.org.dod.internet.private.enterprise.secunet.4.3.1.28 NTP state
            # iso.org.dod.internet.private.enterprise.secunet.4.3.1.29 NTP last updatepolicycnt
            base='.1.3.6.1.4.1.8299.4.3.1',
            oids=[
                '28', # ntp state
                '29', # ntp last update
            ],
        ),
        SNMPTree(
            # iso.org.dod.internet.private.enterprise.secunet.4.3.2.1,1 policy count enabled^
            # iso.org.dod.internet.private.enterprise.secunet.4.3.2.1.2 ipolicy count configured
            base='.1.3.6.1.4.1.8299.4.3.2.1',
            oids=[
                '1', #  enabled
                '2', # configured
            ],
        ),
        SNMPTree(
            # iso.org.dod.internet.private.enterprise.secunet.4.3.2.2,1 ipsec phase 1
            # iso.org.dod.internet.private.enterprise.secunet.4.3.2.2.3 peer count
            # iso.org.dod.internet.private.enterprise.secunet.4.3.2.3.1 ipsec phase 2
            # iso.org.dod.internet.private.enterprise.secunet.4.3.2.3.3 connection count
            base='.1.3.6.1.4.1.8299.4.3.2',
            oids=[
                '2.1', # ipsec phase 1
                '2.3', # peer count 
                '3.1', # ipsec phase 
                '3.3', # connection count
            ],
        ),
        SNMPTree(
            # iso.org.dod.internet.private.enterprise.secunet.4.3.1.24 Active IKE-SA
            base='.1.3.6.1.4.1.8299.4.3.1',
            oids=[
                '24', # active ike-sa
            ],
        ),
    ],
    detect=any_of(
        exists(".1.3.6.1.4.1.2021.4.5.0"),
        exists(".1.3.6.1.4.1.8299.4.3.1.1.0"),
    )
)

def discover_sinal3_system(section):
    """
    Discover the system service for SINA L3.
    """
    if section.get('system'):
        yield Service()

def check_sinal3_system(params, section):
    """
    Check the system service for SINA L3.
    """
    if 'system' in section:
        hsb_mode, hsb_state, hsb_mode_peer, hsb_state_peer = section["system"][0]
        infotext = (
            f"HSB: Mode: {HSB_MODE[int(hsb_mode)]}; State: {STATE[int(hsb_state)]}; "
            f"HSB peer: Mode {HSB_MODE[int(hsb_mode_peer)]}; State {STATE[int(hsb_state_peer)]}"
        )
        if (
            int(hsb_mode) == int(hsb_mode_peer) and int(hsb_state) == 1
        ) or (
            int(hsb_mode_peer) == 3 and int(hsb_state_peer) == 1
        ):
            state = State.WARN
            infotext += " - Error HSB peer"
        elif int(hsb_mode) == int(hsb_mode_peer):
            state = State.OK
            infotext += " - Standalone"
        else:
            state = State.OK
        yield Result(state=state, summary=infotext)

check_plugin_sinal3_system = CheckPlugin(
        name="sinal3_system",
        sections=['sinal3'],
        service_name="System",
        discovery_function=discover_sinal3_system,
        check_function=check_sinal3_system,
        check_default_parameters={},
)

def discover_sinal3_mgmt(section):
    """
    Discover the management service for SINA L3.
    """
    if section.get('mgmt'):
        yield Service()

def check_sinal3_mgmt(params, section):
    """
    Check the management service for SINA L3.
    """
    if "mgmt" in section:
        state = State.OK
        main, fallb, img, srsu_state, srsu_msg  = section["mgmt"][0]
        vinfo = f"Main slot: {main}; Fallback slot: {fallb}"
        sinfo = f"SRSU: State {srsu_state}, {srsu_msg}"
        if main != fallb:
            state = State.WARN
        yield Result(state=state, summary=vinfo)
        state = WARN_TBL[srsu_msg]
        yield Result(state=state, summary=sinfo)


check_plugin_sinal3_mgmt = CheckPlugin(
        name="sinal3_mgmt",
        sections=['sinal3'],
        service_name="Software Versions",
        discovery_function=discover_sinal3_mgmt,
        check_function=check_sinal3_mgmt,
        check_default_parameters={},
)

def discover_sinal3_fans(section):
    """
    Discover the fans service for SINA L3.
    """
    if 'fans' in section:
        for nr, name, rpm in section['fans']:
            if int(rpm) > 0:
                yield Service(item=name)

def check_sinal3_fans(item, params, section):
    """
    Check the fans service for SINA L3.
    """
    if 'fans' in section:
        for nr, name, rpm in section['fans']:
            if name == item:
                name = name.replace(":","_")
                yield from check_levels(
                        float(rpm),
                        metric_name="fan.%s" % name,
                        levels_lower=params.get("lower",(None,None)),
                        levels_upper=params.get("upper",(None,None)),
                        render_func=lambda v: "%d rpm" % int(rpm),
                        label="Speed",
                    )

check_plugin_sinal3_fans = CheckPlugin(
        name="sinal3_fans",
        sections=['sinal3'],
        service_name="Fan %s",
        discovery_function=discover_sinal3_fans,
        check_function=check_sinal3_fans,
        check_default_parameters={ 'lower': (0,0),},
        check_ruleset_name="hw_fans",
)


def discover_sinal3_temp(section):
    """
    Discover the temperature service for SINA L3.
    """
    if 'temperature' in section:
        for nr, name, temp in section['temperature']:
            if int(temp) * 0.001 < 200 and int(temp) * 0.001 > 0:
                yield Service(item=name)

def check_sinal3_temp(item, params, section):
    """
    Check the temperature service for SINA L3.
    """
    if 'temperature' in section:
        for nr, name, temp in section['temperature']:
            if name == item:
                name = name.replace(":","_")
                value_store = get_value_store()
                if int(temp) == 4294839297:
                    temp = 0
                temp = float(temp) * 0.001
                yield from check_temperature(
                        temp,
                        params,
                        value_store=value_store,
                        unique_name="sina_temp.%s" % name
                )

check_plugin_sinal3_temp = CheckPlugin(
        name="sinal3_temp",
        sections=['sinal3'],
        service_name="Temperature %s",
        discovery_function=discover_sinal3_temp,
        check_function=check_sinal3_temp,
        check_default_parameters={},
        check_ruleset_name="temperature",
)


def discover_sinal3_volts(section):
    """
    Discover the voltage service for SINA L3.
    """
    if 'volts' in section:
        for nr, name, temp in section['volts']:
            yield Service(item=name)

def check_sinal3_volts(item, params, section):
    """"
    Check the voltage service for SINA L3.
    """
    if 'volts' in section:
        for nr, name, volts in section['volts']:
            if name == item:
                name = name.replace(":","_")
                volts = float(volts) * 0.001
                yield from check_levels(
                        volts,
                        metric_name="sina_volts.%s" % name,
                        levels_lower=params.get("lower_levels",(None,None)),
                        levels_upper=params.get("levels",(None,None)),
                        render_func=lambda v: "%.2f V" % volts,
                        label="Volts",
                )

check_plugin_sinal3_volts = CheckPlugin(
        name="sinal3_volts",
        sections=['sinal3'],
        service_name="Voltage %s",
        discovery_function=discover_sinal3_volts,
        check_function=check_sinal3_volts,
        check_default_parameters={},
        check_ruleset_name="voltage",
)

def discover_sinal3_gstat(section):
    """
    Discover the global status service for SINA L3.
    """
    if 'global' in section:
        yield Service()

def check_sinal3_gstat(params, section):
    """
    Check the global status service for SINA L3.
    """
    if 'global' in section:
        st, tx = section["global"][0]
        if int(st) != 8:
            state = State.WARN
        else:
            state = State.OK
        yield Result(state=state, summary=tx)


check_plugin_sinal3_gstat = CheckPlugin(
        name="sinal3_gstat",
        sections=['sinal3'],
        service_name="Global status",
        discovery_function=discover_sinal3_gstat,
        check_function=check_sinal3_gstat,
        check_default_parameters={},
)

def discover_sinal3_config(section):
    """
    Discover the configuration versions service for SINA L3.
    """
    if section.get('config'):
        yield Service()

def check_sinal3_config(params, section):
    """
    Check the configuration versions service for SINA L3.
    """
    if section.get('config'):
        active, cfs, smart = section['config'][0]
        infotext = f"Active: {active}; System-CFS: {cfs}; Smartcard: {smart}"
        if active >= cfs or active >= smart:
            state = State.OK
            yield Result(state=state, summary=infotext)
        else:
            state = State.WARN
            infotext += " - Active lower System-CFS or Smartcard"
            yield Result(state=state, summary=infotext)
        if cfs > smart:
            state = State.WARN
            infotext += " - System-CFS > Smartcard"
            yield Result(state=state, summary=infotext)

check_plugin_sinal3_config = CheckPlugin(
        name="sinal3_config",
        sections=['sinal3'],
        service_name="Config versions",
        discovery_function=discover_sinal3_config,
        check_function=check_sinal3_config,
        check_default_parameters={},
)

def discover_sinal3_aclvers(section):
    """
    Discover the ACL versions service for SINA L3.
    """
    if 'aclvers' in section:
        yield Service()

def check_sinal3_aclvers(params, section):
    """"
    Check the ACL versions service for SINA L3.
    """
    if 'aclvers' in section:
        active, smart = section['aclvers'][0]
        infotext = f"Active ACL: {active}; Smartcard ACL: {smart}"
        if active != smart:
            state = State.WARN
        else:
            state = State.OK
        yield Result(state=state, summary=infotext)

check_plugin_sinal3_aclvers = CheckPlugin(
        name="sinal3_aclvers",
        sections=['sinal3'],
        service_name="ACL versions",
        discovery_function=discover_sinal3_aclvers,
        check_function=check_sinal3_aclvers,
        check_default_parameters={},
)

def discover_sinal3_vers(section):
    """
    Discover the version service for SINA L3.
    """
    if 'vers' in section:
        yield Service()

def check_sinal3_vers(params, section):
    """
    Check the version service for SINA L3.
    """
    if 'vers' in section:
        state = State.OK
        active = section['vers'].split("\n")[0].strip()
        infotext = f"Active version: {active}"
        yield Result(state=state, summary=infotext)

check_plugin_sinal3_vers = CheckPlugin(
        name="sinal3_vers",
        sections=['sinal3'],
        service_name="Version",
        discovery_function=discover_sinal3_vers,
        check_function=check_sinal3_vers,
        check_default_parameters={},
)

def discover_sinal3_serial(section):
    """
    Discover the serial service for SINA L3.
    """
    if 'serial' in section:
        if section['serial']:
            yield Service()

def check_sinal3_serial(params, section):
    """
    Check the serial service for SINA L3.
    """
    if 'serial' in section:
        state = State.OK
        serial = section['serial'].strip()
        infotext = f"{serial}"
        yield Result(state=state, summary=infotext)

check_plugin_sinal3_serial = CheckPlugin(
        name="sinal3_serial",
        sections=['sinal3'],
        service_name="Serial",
        discovery_function=discover_sinal3_serial,
        check_function=check_sinal3_serial,
        check_default_parameters={},
)

def discover_sinal3_box(section):
    """
    Discover the box type service for SINA L3.
    """
    if 'box' in section:
        if section['box'] != '':
            yield Service()

def check_sinal3_box(params, section):
    """
    Check the box type service for SINA L3.
    """
    if 'box' in section:
        state = State.OK
        boxtype = section['box'].strip()
        infotext = f"{boxtype}"
        yield Result(state=state, summary=infotext)

check_plugin_sinal3_box = CheckPlugin(
        name="sinal3_box",
        sections=['sinal3'],
        service_name="Box type",
        discovery_function=discover_sinal3_box,
        check_function=check_sinal3_box,
        check_default_parameters={},
)

def discover_sinal3_ntp(section):
    """
    Discover the NTP service for SINA L3.
    """
    if 'ntp' in section:
        yield Service()

def check_sinal3_ntp(params, section):
    """
    Check the NTP service for SINA L3.
    """
    if 'ntp' in section:
        state = State.OK
        st, last = section['ntp'][0]
        infotext = f"State: {NSTATE[int(st)]}; Lasttime updated: {last.strip()}"
        if int(st) < 2:
            state = State.WARN
        elif int(st) > 2:
            state = State.CRIT
        else:
            state = State.OK
        yield Result(state=state, summary=infotext)

check_plugin_sinal3_ntp = CheckPlugin(
        name="sinal3_ntp",
        sections=['sinal3'],
        service_name="NTP",
        discovery_function=discover_sinal3_ntp,
        check_function=check_sinal3_ntp,
        check_default_parameters={},
)

def discover_sinal3_policycnt(section):
    """
    Discover the policy count service for SINA L3.
    """
    if 'policycnt' in section:
        yield Service()

def check_sinal3_policycnt(params, section):
    """
    Check the policy count service for SINA L3.
    """
    if 'policycnt' in section:
        ev, ec = section['policycnt'][0]
        ev = int(ev)
        ec = int(ec)
        yield Metric("policy_enabled", ev)
        yield Metric("policy_configured", ec)
        infotext = f"enabled: {ev}; configured: {ev}"
        yield Result(state=State.OK,summary=infotext)

check_plugin_sinal3_sinal3_policycnt = CheckPlugin(
        name="sinal3_policycnt",
        sections=['sinal3'],
        service_name="Policy count",
        discovery_function=discover_sinal3_policycnt,
        check_function=check_sinal3_policycnt,
        check_default_parameters={},
)

def discover_sinal3_ipsec(section):
    """
    Discover the IPsec service for SINA L3.
    """
    if 'ipsec' in section:
        one, peer, two, con = section['ipsec'][0]
        yield Service(item="IPsec phase one childs")
        yield Service(item="IPsec phase two childs")
        if peer.strip() != "":
            yield Service(item="IPsec peer count")
        if con.strip() != "":
            yield Service(item="IPsec connection count")

def check_sinal3_ipsec(item, params, section):
    """
    Check the IPsec service for SINA L3.
    """
    if 'ipsec' in section:
        one, peer, two, con = section['ipsec'][0]
        one = int(one)
        two = int(two)
        if item == "IPsec phase one childs":
            infotext = f"Count: {one}"
            yield Metric("count_one", one)
            yield Result(state=State.OK,summary=infotext)
        if item == "IPsec phase two childs":
            infotext = f"Count: {two}"
            yield Metric("count_two", two)
            yield Result(state=State.OK,summary=infotext)
        if item == "IPsec peer count":
            peer = int(peer)
            infotext = f"Count: {peer}"
            yield Metric("count_peer", peer)
            yield Result(state=State.OK,summary=infotext)
        if item == "IPsec connection count":
            con = int(con)
            infotext = f"Count: {con}"
            yield Metric("count_con", con)
            yield Result(state=State.OK,summary=infotext)

check_plugin_sinal3_ipsec = CheckPlugin(
        name="sinal3_ipsec",
        sections=['sinal3'],
        service_name="%s",
        discovery_function=discover_sinal3_ipsec,
        check_function=check_sinal3_ipsec,
        check_default_parameters={},
)

def discover_sinal3_ike_sa(section):
    """
    Discover the IKE-SA service for SINA L3.
    """
    if 'ike-sa' in section:
        if section['ike-sa'] != '':
            yield Service()

def check_sinal3_ike_sa(params, section):
    """
    Check the IKE-SA service for SINA L3.
    """
    if 'ike-sa' in section:
        cnt = int(section['ike-sa'][0])
        yield Metric("ike_sa", cnt)
        infotext = f"Number of established connections: {cnt}"
        yield Result(state=State.OK,summary=infotext)

check_plugin_sinal3_ike_sa = CheckPlugin(
        name="sinal3_ike_sa",
        sections=['sinal3'],
        service_name="Active IKE-SA",
        discovery_function=discover_sinal3_ike_sa,
        check_function=check_sinal3_ike_sa,
        check_default_parameters={},
)
