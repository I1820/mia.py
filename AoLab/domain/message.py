# In The Name Of God
# ========================================
# [] File Name : message.py
#
# [] Creation Date : 18-09-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================


class AoLabThingMessage:
    def __init__(self, node_id: int, battery: int, *things):
        self.node_id = node_id
        self.battery = battery
        self.things = things
