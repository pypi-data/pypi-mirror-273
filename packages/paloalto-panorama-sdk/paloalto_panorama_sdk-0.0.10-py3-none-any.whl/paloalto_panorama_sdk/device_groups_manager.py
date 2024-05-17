import json

import requests


class DeviceGroupsManager:
    def __init__(self, panorama_url, api_key, verify=True):
        self.panorama_url = panorama_url
        self.api_key = api_key
        self.verify = verify
        self.url = f"{self.panorama_url}/restapi/v10.2/Panorama/DeviceGroups"
        self.headers = {'Content-Type': 'application/json',
                        'X-PAN-KEY': f"{self.api_key}"}

    def list_device_groups(self):
        response = requests.get(self.url, headers=self.headers, verify=self.verify)
        device_groups = json.loads(response.content.decode('utf-8'))
        return device_groups

