#!/usr/bin/env python
# Service NOW
# Bluk: no

import sys
import requests
from requests.auth import HTTPBasicAuth
#from cmk.notification_plugins import utils


API_URL = "https://a1kit.service-now.com/api/x_segh4_cxn/connect/transaction_queue/checkmk/incident/create"
AUTH_USER = ""
AUTH_PASSWORD = ""


def main():
    """
    Main part to sendout notification
    """

    auth = HTTPBasicAuth(AUTH_USER, AUTH_PASSWORD)
    #context = utils.collect_context()
    context = {}

    host_name = context['HOSTNAME']
    site_name = context['OMD_SITE']
    contacts = context['CONTACTS']
    service_account = site_name
    event_time = context['MICROTIME']
    long_plugin_output = ""

    if context['WHAT'] == "HOST":
        mngmt_pack = {
            "hostname": host_name,
            "contacts" : contacts,
            }
        source_id = "{}|{}".format(site_name, host_name)
        serverity = context['HOSTNAME']
        plugin_output = context['HOSTOUTPUT']
    else:
        service_name = context['SERVICEDESC']
        mngmt_pack = {
            "hostname": host_name,
            "servicename" : service_name,
            "contacts" : contacts,
            }
        source_id = "{}|{}|{}".format(site_name, host_name, service_name)
        serverity = context['SERVICESTATE']
        plugin_output = context['SERVICEOUTPUT']

    payload = {
        "QUELLE" : "Checkmk",
        "QUELLEID": source_id,
        "ZIEL" : "ServiceNow",
        "FUNKTION" : "create",
        "FQDN" : host_name,
        "MP" : mngmt_pack,
        "SERVERITY" : serverity,
        "DIENSTKONTO" : service_account,
        "EVENTZEITPUNKT" : event_time,
        "KURZBESCHREIBUNG" : plugin_output,
        "LANGBESCHREIBUNG" : long_plugin_output,
    }


    try:
        response = requests.post(API_URL, json=payload, auth=auth)
    except Exception as e: #pylint: disable=broad-except, invalid-name
        print(e)
        print(response.json())
        sys.exit(2)
    sys.exit(0)

main()
