# In The Name Of God
# ========================================
# [] File Name : log.py
#
# [] Creation Date : 04-09-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
import datetime
import requests


class I1820Log:
    def __init__(self, data: dict):
        self.states = data
        self.timestamp = datetime.datetime.now()
        self.endpoint = ""

    def send(self):
        log = {
            "timestamp": self.timestamp.timestamp(),
            "data": {"states": self.states},
            "endpoint": self.endpoint
        }
        requests.post('http://192.168.1.9:1373/log', json=log)
