import json
import requests
from paloalto_panorama_sdk.panorama_data_kit.security_post_rule_data import SecurityPostRule


class SecurityPostRulesManager:
    def __init__(self, panorama_url, api_key, verify=True):
        self.panorama_url = panorama_url
        self.api_key = api_key
        self.verify = verify
        self.url = f"{self.panorama_url}/restapi/v10.2/Policies/SecurityPostRules"
        self.headers = {'Content-Type': 'application/json',
                        'X-PAN-KEY': f"{self.api_key}"}

    def get_security_post_rules(self, location='shared', device_group='TestGroup'):
        post_rules_list = self.list_post_rules(location=location, device_group=device_group)
        post_rules: [SecurityPostRule] = []
        for post_rule in post_rules_list:
            post_rules.append(post_rule)
        return post_rules

    def post_security_post_rule(self, security_post_rule: SecurityPostRule):
        decoded_security_post_rule = self.create_post_rules(
            device_group=security_post_rule.device_group,
            name=security_post_rule.name,
            action=security_post_rule.action,
            description=security_post_rule.description,
            from_zone=security_post_rule.from_member,
            source_group=security_post_rule.source_member,
            to_zone=security_post_rule.to_member,
            destination_group=security_post_rule.destination_member,
            service=security_post_rule.service_member,
            profile_type=security_post_rule.profile_type,
            profile=security_post_rule.profile_setting
        )

    def list_post_rules(self, location='shared', device_group='TestGroup'):
        params = {'location': location, 'device-group': device_group}
        response = requests.get(url=self.url, headers=self.headers, params=params, verify=self.verify)
        post_rules = json.loads(response.content.decode('utf-8'))
        return post_rules

    def create_post_rules(self, device_group, name, action, description, from_zone, source_group,
                          to_zone, destination_group, service, profile_type, profile):
        location = "shared" if device_group == 'shared' else "device-group"
        params = {'name': name, 'location': location, 'device-group': device_group}
        payload = self._get_post_rules_payload(device_group, name, action, description, from_zone, source_group,
                                               to_zone, destination_group, service, profile_type, profile)
        response = requests.post(url=self.url, headers=self.headers, params=params, data=json.dumps(payload),
                                 verify=self.verify)
        return json.loads(response.content.decode('utf-8'))

    @staticmethod
    def _get_post_rules_payload(device_group, name, action, description, from_zone, source_group,
                                to_zone, destination_group, service, profile_type, profile):
        security_policy_payload = {
            "entry": [
                {
                    "@location": device_group,
                    "@name": name,
                    "description": description,
                    "@vsys": "vsys1",
                    "action": action,
                    "log-setting": "default",
                    "from": {
                        "member": [
                            from_zone.split('\n')
                        ]
                    },
                    "to": {
                        "member": [
                            to_zone.split('\n')
                        ]
                    },
                    "source": {
                        "member": [
                            source_group.split('\n')
                        ]
                    },
                    "destination": {
                        "member": [
                            destination_group.split('\n')
                        ]
                    },
                    "service": {
                        "member": [
                            service.split('\n')
                        ]
                    },
                    "application": {
                        "member": [
                            "any"
                        ]
                    },
                    "tag": {
                        "member": [
                            "to_be_reviewed"
                        ]
                    },
                    'profile-setting': {
                        profile_type: {
                            'member': [
                                profile
                            ]
                        }
                    }
                }
            ]
        }
        return security_policy_payload
