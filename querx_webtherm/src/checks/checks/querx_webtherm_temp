#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-


def inventory_querx_webtherm_temp(info):
    return [("Sensor", {})]

def check_querx_webtherm_temp(item, params, info):
    value = float(info[0][0]) / 10
    return check_temperature(value, params, 'temperature')


check_info["querx_webtherm_temp"] = {
    #'default_levels_variable'   : "querx_webtherm_defaultlevels",
    'inventory_function'        : inventory_querx_webtherm_temp,
    'check_function'            : check_querx_webtherm_temp,
    'service_description'       : 'Temperature %s',
    'has_perfdata'              : True,
    'snmp_info'                 : (".1.3.6.1.4.1.3444.1.14.1.2.1.5", [1]),
    'snmp_scan_function'        : lambda oid:  "Querx" in oid(".1.3.6.1.2.1.1.1.0"),
    'group'                     : 'temperature',
    'includes'                  : [ 'temperature.include' ],
}

