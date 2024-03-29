#!/usr/bin/env python3
# SMS Eagle Appliance
"""
Sms Eagle
"""
# pylint: disable=too-many-locals, import-error, broad-exception-raised, bare-except
import sys
import requests
from cmk.notification_plugins import utils
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

class NotifyEagle():
    """
    Eagle Notification Class
    """

    def __init__(self):
        """
        Perpare Config and Params
        """
        context = utils.collect_context()
        self.config = {
            'api_host': context['PARAMETER_API_HOST'],
            'username': context['PARAMETER_USERNAME'],
            'password': context['PARAMETER_PASSWORD']
        }
        self.context = context


    def get_message(self):
        """
        Build SMS Text
        """

        messages = []
        messages.append(self.context['HOSTNAME'])
        if self.context['WHAT'] == 'HOST':
            messages.append(self.context['HOSTSTATE'])
            messages.append(self.context['HOSTOUTPUT'])
        else:
            messages.append(self.context['SERVICESTATE'])
            messages.append(self.context['SERVICEDESC'])
            messages.append(self.context['SERVICEOUTPUT'])

        return " ".join(messages)[:160]

    def notify(self):
        """
        Main part
        """
        url = f"{self.config['api_host']}/index.php/http_api/send_sms"

        params = {
            'login': self.config['username'],
            'pass': self.config['password'],
            'to': self.context['CONTACTPAGER'],
            'message': self.get_message(),

        }
        response = requests.get(url, params=params, verify=False, timeout=10)
        print(response.text)
        if response.status_code != 200:
            return 1
        return 0

if __name__ == "__main__":
    notify = NotifyEagle()
    sys.exit(notify.notify())
