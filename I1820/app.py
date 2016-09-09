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
from . import wapp

import flask
import json
import requests
import threading


class I1820App(threading.Thread):
    notification_handlers = {}

    def __init__(self, i1820_ip: str, i1820_port: int):
        self.base_url = "http://%s:%d/" % (i1820_ip, i1820_port)
        self.things = []
        I1820App.notification_handlers = {}
        threading.Thread.__init__(self)

    def add_thing(self, type, id):
        self.things.append({'type': type, 'id': id})

    def run(self):
        PingService(self.base_url, self.things).ping()
        wapp.run(debug=False, host="0.0.0.0", port=1373)

    def notification(self, thing: str):
        def _notification(fn):
            self.notification_handlers[thing] = fn
            return fn
        return _notification

    def log(self, log: I1820Log):
        log = {
            "timestamp": log.timestamp.timestamp(),
            "type": log.type,
            "device": log.device,
            "data": {"states": log.states},
            "endpoint": log.endpoint
        }
        requests.post(self.base_url + 'log', json=log)

    @classmethod
    def notification_handler(cls, data: dict):
        results = {}
        try:
            results = cls.notification_handlers[data['type']](data)
        except KeyError:
            pass
        return results


@wapp.route('/event', methods=['POST'])
def notification_handler():
    data = flask.request.get_json(force=True)
    result = I1820App.notification_handler(data)
    return json.dumps(result)
