#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-


def inventory_querx_webtherm_humidity(info):
    return [("Sensor", {})]

def check_querx_webtherm_humidity(item, params, info):
    value = float(info[0][0]) 
    return check_humidity(value, params)


check_info["querx_webtherm_humidity"] = {
    #'default_levels_variable'   : "querx_webtherm_defaultlevels",
    'inventory_function'        : inventory_querx_webtherm_humidity,
    'check_function'            : check_querx_webtherm_humidity,
    'service_description'       : 'Humidity %s',
    'has_perfdata'              : True,
    'snmp_info'                 : (".1.3.6.1.4.1.3444.1.14.1.2.1.5", [2]),
    'snmp_scan_function'        : lambda oid:  "Querx" in oid(".1.3.6.1.2.1.1.1.0"),
    'group'                     : 'humidity',
    'includes'                  : [ 'humidity.include' ],
}

