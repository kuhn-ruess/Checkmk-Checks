#!/usr/bin/env python3
"""
Script to Add or Remove Labels from CMK1 Versions
"""
import sys
import requests



CMK_SITE = 'http://monsrv/mon'
USERNAME = 'automation'
SECRET = '48369317-7274-4459-abf2-9ebca96b0e3a'


if len(sys.argv) < 4:
    print("Usage: edit_label.py add|remove hostname|-f hostfile label:name")
    sys.exit(1)


op = sys.argv[1]
hostname = sys.argv[2]

input_file = False
if hostname == '-f':
    input_file = sys.argv[3]
    label_str = sys.argv[4]
else:
    label_str = sys.argv[3]
label_name, label_value = label_str.split(':')

def make_request(what, payload):
    """
    Generic function to contact the api
    """
    conf = {
        'site' : CMK_SITE,
        'action' : what,
        'username' : USERNAME,
        'secret' : SECRET,
    }

    url = '{site}/check_mk/webapi.py' \
          '?action={action}&_username={username}' \
          '&_secret={secret}&output_format=python&request_format=python'.format(**conf)

    if payload: # payload is not empty
        formated = ascii(payload).replace(" '", " u'")
        formated = formated.replace("{'", "{u'")
    else: # payload is empty
        formated = ascii(payload)

    response = requests.post(url, {"request": formated}, verify=False)
    return eval(response.text) #pylint: disable=eval-used

def run(input_hostname):
    """
    Run Operations
    """

    host_data = make_request('get_host', {'hostname' : input_hostname})['result']

    if op == 'remove':
        if 'labels' in host_data['attributes']:
            try:
                del host_data['attributes']['labels'][label_name]
            except KeyError:
                pass
    elif op == 'add':
        host_data['attributes'].setdefault('labels', {})
        host_data['attributes']['labels'][label_name] = label_value

    del host_data['path']
    resp = make_request('edit_host', host_data)
    print(input_hostname +" "+str(resp))

if input_file:
    for line in open(input_file).readlines():
        hostname = line.strip()
        run(hostname)
else:
    run(hostname)
