#!/usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

from sys import argv
from requests import post
from requests.auth import HTTPBasicAuth


class AgentJson():
    """
    Agent Json
    """

    def __init__(self, api_host, user, password):
        """
        Init
        """
        self.api_host = api_host
        self.auth = HTTPBasicAuth(user, password)


    def get_json(self):
        """
        Get JSON Stream
        """

        map_states = {
                'UP' : 0,
        }

        response = post(self.api_host, auth=self.auth, timeout=30)
        checks = response.json()['checks']

        print("<<<local>>>")
        for check in checks:
            summary = ", ".join([f"{x}: {y}" for x, y in check['data'].items()])
            print(f"{map_states.get(check['status'], 2)} {check['name']} - {summary}")


if __name__ == "__main__":
    aj = AgentJson(argv[1], argv[2], argv[3])
    aj.get_json()
