# In The Name Of God
# ========================================
# [] File Name : I1820App.py
#
# [] Creation Date : 09-09-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
from .log.log import I1820Log
from .bootstrap.ping import PingService
from .bootsrap.route import app
import requests
import threading


class I1820App(threading.Thread):
    def __init__(self, i1820_ip: str, i1820_port: int):
        self.notification_handlers = {}
        self.base_url = "http://%s:%d/" % (i1820_ip, i1820_port)
        self.things = []

    def add_thing(self, type, id):
        self.things.append({'type': type, 'id': id})

    def run(self):
        PingService(self.base_url, self.things).ping()
        app.run(debug=True, host="0.0.0.0", port=1373)

    def notification(self, thing: str):
        def _notification(fn):
            self.notification_handlers[thing] = fn
            return fn
        return _notification

    def log(self, log: I1820Log):
        log = {
            "timestamp": log.timestamp.timestamp(),
            "data": {"states": log.states},
            "endpoint": log.endpoint
        }
        requests.post(self.base_url + 'log', json=log)
