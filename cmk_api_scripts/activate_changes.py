#!/usr/bin/env python3
"""
Simple Script to trigger Activate Changes e.g. by Cronjob

Bastian Kuhn, bastian.kuhn@kuhn-ruess.de
"""
import sys
import requests

SERVER_ADDRESS = "http://192.168.178.22:5002/cmk"
USERNAME = "cmkadmin"
PASSWORD = "Test123$"
VERIFY_SSL = False
TIMEOUT=15

DEBUG = False

for arg in sys.argv:
    if arg == '-d':
        DEBUG = True

def print_debug(what):
    """
    Print String if Debug is set
    """
    if DEBUG:
        print(f"DEBUG: {what}")

try:
    print("Started Activate Changes")
    base_url = f'{SERVER_ADDRESS}/check_mk/api/1.0/'
    base_headers = {
        'Authorization': f"Bearer {USERNAME} {PASSWORD}"
    }

    # Get current activation etag
    print(" - Get current Pending Changes")
    url = base_url +  "/domain-types/activation_run/collections/pending_changes"
    response = requests.get(url, headers=base_headers, verify=VERIFY_SSL, timeout=TIMEOUT)
    print_debug(response.json())
    etag = response.headers.get('ETag')
    if not response.json()['value']:
        print(" - Nothing todo, end")
        sys.exit(0)

    activate_headers = {
        'if-match': etag
    }
    activate_headers.update(base_headers)

    # Trigger Activate Changes
    print(" - Trigger Activate Changes")
    url = base_url + "/domain-types/activation_run/actions/activate-changes/invoke"
    json = {
        'redirect': False,
        'force_foreign_changes': True,
    }
    response = requests.post(url, json=json, headers=activate_headers,
                             verify=VERIFY_SSL, timeout=TIMEOUT)

    print_debug(response.json())
    response_json = response.json()
    if 'id' not in response_json:
        print("Cant activate Changes currently, try again")
        sys.exit(1)

    activation_id = response_json['id']


    # Wait and Check for Status
    print(" - Wait for Activation")
    url = \
        f"{base_url}/objects/activation_run/{activation_id}/actions/wait-for-completion/invoke"
    response = requests.get(url, headers=base_headers, verify=VERIFY_SSL, timeout=TIMEOUT)
    if response.status_code != 204:
        print("Activation not possible, see details below")
        print(response.json())
        sys.exit(1)

    print(" -- Done")

    print_debug(f"Activation Response: {response.status_code}")
    print("Ended Activate Changes")
except Exception as error: #pylint: disable=broad-exception-caught
    print(f"Error: {error}")
    if DEBUG:
        raise
