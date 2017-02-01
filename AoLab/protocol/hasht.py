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
        'lamp': 'l',
        'cooler': 'c',
        'curtain': 'k'
    }

    def marshal(self, type, device_id, node_id, command) -> str:
        return '@%s,%s%s%s.' % (node_id, self.thing_actuators[type],
                                device_id, command)

    def unmarshal(self, message: str) -> AoLabThingMessage:
        if len(message) == 0 or message[0] != '@':
            return None
        parts = message.split(',')
        node = parts[0][1:]
        battery = parts[-1][:-2]
        try:
            battery = (int(battery) - 2900) // 13
        except (KeyError, ValueError):
            battery = 0
        things = []
        for thing in parts[1:-1]:
            things.append({
                'type': self.thing_sensors[thing[0]],
                'value': thing[2:],
                'device': thing[1]
            })
        return AoLabThingMessage(node, battery, *things)
