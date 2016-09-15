# In The Name Of God
# ========================================
# [] File Name : I1820App.py
#
# [] Creation Date : 09-09-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
from .domain.log import I1820Log, I1820LogJSONEncoder
from .bootstrap.ping import PingService
from . import wapp
from . import i1820_id

import flask
import json
import requests
import threading
from werkzeug.utils import secure_filename


class I1820App(threading.Thread):
    notification_handlers = {}

    def __init__(self, i1820_ip: str, i1820_port: int,
                 i1820p_ip: str=None, i1820p_port: int=None):
        self.base_url = "http://%s:%d/" % (i1820_ip, i1820_port)
        self.things = []
        self.host = "0.0.0.0" if i1820p_ip is None else i1820p_ip
        self.port = 1373 if i1820p_port is None else i1820p_port
        I1820App.notification_handlers = {}
        threading.Thread.__init__(self)

    def add_thing(self, type, id, attributes={}):
        self.things.append({'type': type, 'id': id, 'attributes': attributes})

    def run(self):
        PingService(self.base_url, self.things).ping()
        wapp.run(debug=False, host=self.host, port=self.port)

    def notification(self, thing: str):
        def _notification(fn):
            self.notification_handlers[thing] = fn
            return fn
        return _notification

    def log(self, type, device, states):
        log = I1820Log(type, device, states, str(i1820_id))
        requests.post(self.base_url + 'log',
                      data=I1820LogJSONEncoder().encode(log))

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


@wapp.route('/upload', methods=['POST'])
def upload_handler():
    f = flask.request.files['target']
    f.save('' + secure_filename(f.filename))
