import json
from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class DeviceGroup:
    name: str
    description: str
    devices: str

    def to_json(self):
        data_dict = asdict(self)
        data_dict['@name'] = data_dict.pop('name')
        return json.dumps(data_dict, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_data):
        name = json_data.get('@name')
        description = json_data.get('description')
        devices = json_data.get('devices')
        return cls(name, description, devices)
