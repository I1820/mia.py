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
    def handler(self, message: str):
        parts = message.split(',')
        node = parts[0][1:]
        battery = parts[-1][:-1]
        things = []
        for thing in parts[1:-1]:
            things.append({
                'type': thing[0],
                'value': thing[2:],
                'device': thing[1]
            })
        AoLabThingMessage(node, battery, *things)

    def process(self):
        pass
