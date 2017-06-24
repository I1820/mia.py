# In The Name Of God
# ========================================
# [] File Name : hasht.py
#
# [] Creation Date : 18-09-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
from .base import AoLabSerialProtocol
from ..domain.message import AoLabThingMessage


class HashtProtocol(AoLabSerialProtocol):

    thing_sensors = {
        't': 'temperature',
        'l': 'light',
        'h': 'humidity',
        'm': 'motion',
        'g': 'gas'
    }

    thing_actuators = {
        'alarm': 'A',
        'lamp': 'l',
        'cooler': 'c',
        'curtain': 'p',
        'projector': 'p',
        'tv': 't',
        'valve': 'v'
    }

    def marshal(self, type, device_id, node_id, command) -> str:
        if type == 'lamp' or type == 'curtain' or type == 'alarm' or type == 'valve':
            return '@%s,%s%s%s.' % (node_id, self.thing_actuators[type],
                                    device_id, command)
        if type != 'lamp':
            return '@%s,%s%s.' % (node_id, self.thing_actuators[type], command)

    def unmarshal(self, message: str) -> AoLabThingMessage:
        if len(message) == 0 or message[0] != '@':
            return None
        parts = message.split(',')
        node = parts[0][1:]
        if parts[-1][0].isalpha():
            battery = 0
            parts[-1] = parts[-1][:-2]
        else:
            battery = parts[-1][:-2]
            parts.pop()
            try:
                battery = (int(battery) - 2900) // 13
            except (KeyError, ValueError):
                battery = 0
        things = []
        for thing in parts[1:]:
            things.append({
                'type': self.thing_sensors[thing[0]],
                'value': thing[2:],
                'device': thing[1]
            })
        return AoLabThingMessage(node, battery, *things)
