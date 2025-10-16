#!/usr/bin/env python3
"""
Cleanup Tool for Eventconsole.

I case the EC is full of events for services already OK in Checkmk,
this tool sends this Events to Archive.

Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

import argparse
import requests
from os import environ

class Checkmk():

    status_cache = {}

    def __init__(self, config):
        """
        Set Credentials
        """
        self.address = config['address']
        self.username = config['username']
        self.password = config['password']
        self.verify = config['verify']

    def request(self, endpoint, method="GET", json=None):
        """
        Requests to Checkmk
        """

        url = f'{self.address}/check_mk/api/1.0/{endpoint}'
        headers = {
            'Authorization': f'Bearer {self.username} {self.password}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }


        if method == "GET":
            response = requests.get(url, headers=headers, verify=self.verify)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=json, verify=self.verify)

        try:
           response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            response_json = {}

        return response_json

    def get_events(self):
        """
        Return all Events based on a services
        """
        events = self.request("/domain-types/event_console/collections/all")
        for event in events['value']:
            event_id = event['id']
            event = event['extensions']
            event_dict = {
                "service_description": event['application'],
                "host_name": event['host'],
                "event_id": event_id,
                "site_id": event['site_id'],
            }
            yield event_dict


    def get_service_state(self, host_name, service_description):
        """
        Return Service information for given host
        """
        cache_id = (host_name, service_description)
        if cache_id in self.status_cache:
            return self.status_cache[cache_id]
        url = (
                f"/objects/host/{host_name}/actions/show_service/invoke?"
                f"service_description={service_description}&columns=state"
        )
        service_data = self.request(url)
        state = service_data['extensions']['state']
        self.status_cache[cache_id] = state
        return state

    def get_host_state(self, host_name):
        """
        Return State for given Hostname
        """
        cache_id = (host_name, "HOST")
        if cache_id in self.status_cache:
            return self.status_cache[cache_id]
        url = (
                f"/objects/host/{host_name}?"
                f"columns=state"
        )
        service_data = self.request(url)
        state = service_data['extensions']['state']
        self.status_cache[cache_id] = state
        return state 


    def close_event(self, event_id, cmk_site):
        """
        Close given Event ID
        """
        url = f"/domain-types/event_console/actions/delete/invoke"
        json={
            "filter_type": "by_id",
            "event_id": event_id,
            "site_id": cmk_site
        }

        self.request(url, "POST", json)


    def sync_ec_data(self):
        """
        Sync Status of EC Events with Checkmk Services
        """
        ids_to_close = []
        for event in self.get_events():
            if event['service_description'] == "HOST":
                state = self.get_host_state(event['host_name'])
            else:
                state = self.get_service_state(event['host_name'], event['service_description'])

            if state == 0:
                print(f"OK-> ID: {event['event_id']} ({event['host_name']}, {event['service_description']})")
                ids_to_close.append((event['event_id'], event['site_id']))
            else:
                print(f"Error-> ID: {event['event_id']} ({event['host_name']}, {event['service_description']})")

        close_events = input("Enter yes to close the events: ")
        if close_events.lower() == 'yes':
            for event_id, site_id in ids_to_close:
                print(f"Closing ID {event_id}")
                self.close_event(event_id, site_id)
                print("--> done")

def get_automation_password():
    """
    Get local Automation user
    """
    with open(f"{environ.get('OMD_ROOT')}/var/check_mk/web/automation/automation.secret", "r") as f:
        data = f.read()
        f.close()
    return data.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='EC Cleanup tool. Cleans Events for Services OK in Checkmk')
    parser.add_argument('--user', dest='user', required=False, help='Checkmk Admin Username')
    parser.add_argument('--password', dest='password', required=False, help='Password or Automation Token')
    parser.add_argument('--site-url', dest='url', required=False, help='Url to checkmk site, https://hostname/sitename')

    args = parser.parse_args()

    if not args.user:
        ## Get from Environment
        user = 'automation'
        password = get_automation_password()
        address = f"http://localhost/{environ['OMD_SITE']}"
        verify = False

    else:
        user = args.user
        address = args.url
        password = args.password
        verify = True

    config = {
        'address': address,
        'username': user,
        'password': password,
        'verify': verify,
    }
    cmk = Checkmk(config)
    cmk.sync_ec_data()