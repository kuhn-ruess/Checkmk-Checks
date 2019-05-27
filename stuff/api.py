#!/usr/bin/env python3
"""
Example script to communicate with CheckMK WebAPI
"""
import requests

def make_request(what, payload):
    """
    Generic function to contact the api
    """
    conf = {
        'host' : 'monsrv',
        'action' : what,
        'username' : 'automation',
        'secret' : '97effb6f-a6b3-46d5-8914-73a9cbf42f4c',
    }

    url = 'http://{host}/mon/check_mk/webapi.py' \
          '?action={action}&_username={username}' \
          '&_secret={secret}&output_format=python&request_format=python'.format(**conf)
    response = requests.post(url, 'request='+str(payload))
    return eval(response.text) #pylint: disable=eval-used

# HOST_DATA = make_request('get_host', {'hostname' : 'localhost'})['result']
# HOST_DATA['attributes']['tag_os'] = 'lnx'
# del HOST_DATA['path']

# print(make_request('edit_host', HOST_DATA))

REQUEST = {
    'hostname' : 'linux-box',
    'mode' : 'fixall',
}

print(make_request('discover_services', REQUEST))

REQUEST = {
    'mode': 'dirty',
    'sites': [],
    'allow_foreign_changes': '1',
    'comment': 'Aenderungen aus der WebAPI.'
}

print(make_request('activate_changes', REQUEST))
