#!/usr/bin/env python3
# Rediscover service

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from os import environ
from requests import Session


def get_user():
    with open(f"{environ.get('OMD_ROOT')}/var/check_mk/web/automation/automation.secret", "r") as f:
        data = f.read()
        f.close()

    return ["automation", data.strip()]


def get_discovery(username, password, url, host, service):
    session = Session()
    session.headers['Authorization'] = f"Bearer {username} {password}"
    session.headers['Accept'] = 'application/json'

    resp = session.get(
        f"{url}/objects/service_discovery/{host}",
    )
    
    if resp.status_code == 200:
        data = resp.json()
        services = data["extensions"]["check_table"]

        for item in services.keys():
            if services[item]["id"] == service:
                return services[item]["links"][1]["body_params"]
    else:
        print("ERROR: Could not get discovery information")
        return False


def update_discovery(username, password, url, host, content):
    session = Session()
    session.headers['Authorization'] = f"Bearer {username} {password}"
    session.headers['Accept'] = 'application/json'

    resp = session.put(
        f"{url}/objects/host/{host}/actions/update_discovery_phase/invoke",
        headers = {
            "Content-Type": 'application/json',
        },
        json = content,
    )

    if resp.status_code == 204:
        return True
    else:
        return False


def activate_changes(username, password, url):
    session = Session()
    session.headers['Authorization'] = f"Bearer {username} {password}"
    session.headers['Accept'] = 'application/json'
    session.max_redirects = 100  # increase if necessary

    resp = session.get(
        f"{url}/domain-types/activation_run/collections/pending_changes",
    )

    if resp.status_code == 200:
        etag = resp.headers["ETag"]
    else:
        etag = None

    resp = session.post(
        f"{url}/domain-types/activation_run/actions/activate-changes/invoke",
        headers = {
            "If-Match": f'{etag}',
            "Content-Type": 'application/json',
        },
        json = {
            "redirect": False,
            "sites": [],
            "force_foreign_changes": True,
        },
        allow_redirects = True,
    )

    if resp.status_code == 200 or resp.status_code == 204 or resp.status_code == 302 or resp.status_code == 422:
        pass
    else:
        print("ERROR: Failed activate changes")


if "SERVICE" == environ.get("NOTIFY_WHAT", "NA"):
    # API configuration
    API_PROTO = environ.get("NOTIFY_PARAMETER_PROTO", "http")
    API_HOSTNAME = environ.get("NOTIFY_PARAMETER_HOSTNAME", "localhost")
    API_SITENAME = environ.get("NOTIFY_PARAMATER_SITENAME", environ.get("OMD_SITE"))
    API_URL = f"{API_PROTO}://{API_HOSTNAME}/{API_SITENAME}/check_mk/api/1.0"

    try:
        API_USERNAME, API_PASSWORD = get_user()
    except:
        print("ERROR: Could not get user credentials")
        exit(1)

    HOSTNAME = environ.get("NOTIFY_HOSTNAME", "NA")
    SERVICENAME = environ.get("NOTIFY_SERVICEDESC", "NA")
    SERVICESTATE = environ.get("NOTIFY_SERVICESTATE", "NA")

    body_json = get_discovery(API_USERNAME, API_PASSWORD, API_URL, HOSTNAME, SERVICENAME)

    if body_json:
        if update_discovery(API_USERNAME, API_PASSWORD, API_URL, HOSTNAME, body_json):
            body_json["target_phase"] = "monitored"

            if update_discovery(API_USERNAME, API_PASSWORD, API_URL, HOSTNAME, body_json):
                activate_changes(API_USERNAME, API_PASSWORD, API_URL)
            else:
                print("ERROR: Could not made service monitored again")
        else:
            print("ERROR: Could not made service undecided")
