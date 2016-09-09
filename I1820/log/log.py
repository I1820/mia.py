# In The Name Of God
# ========================================
# [] File Name : log.py
#
# [] Creation Date : 04-09-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
import datetime
from .. import i1820_id


class I1820Log:
    def __init__(self, data: dict):
        self.states = data
        self.timestamp = datetime.datetime.now()
        self.endpoint = str(i1820_id)
