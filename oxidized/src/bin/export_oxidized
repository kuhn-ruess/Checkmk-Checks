#!/usr/bin/env python3

from os import getenv
from json import dumps
from re import search
from requests import Session

username = "oxidized"
secret = None
url = "https://016-mon-001/mon"
session = None
data = {}

if not secret:
    with open(
        f"{getenv('OMD_ROOT', '')}/var/check_mk/web/{username}/automation.secret"
    ) as passwd:
        secret = passwd.read().strip()

headers = {
    "Authorization": f"Bearer {username} {secret}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

if not session:
    session = Session()

response = session.request(
    method="GET",
    url=f"{url}/check_mk/view.py?view_name=oxidized_hosts&output_format=json",
    headers=headers,
)

if response.status_code >= 300 or "ERROR" in response.text:
    print(f"Request failed: {response.text}")

else:
    data = response.json()
    data_list = []

    for line in data[1:]:
        match = search(r"\[([A-Za-z0-9_]+)\]", line[1])
        data_list.append({
            'hostname' : line[0],
            'os' : match.group(1),
        })
    print (dumps(data_list, indent=3))
