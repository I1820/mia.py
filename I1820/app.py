# In The Name Of God
# ========================================
# [] File Name : I1820App.py
#
# [] Creation Date : 09-09-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
from .domain.log import I1820Log
from .domain.notif import I1820Notification
from .bootstrap.ping import PingService

import paho.mqtt.client as mqtt
import uuid
import bson

i1820_id = uuid.uuid5(uuid.NAMESPACE_URL,
                      'I1820://%s.aolab.ceit.aut.ac.ir' % uuid.getnode())
token = '83DB8F6299E0A303730B5F913B6A3DF420EBC2C2'


class I1820App:
    def __init__(self, mqtt_ip: str, mqtt_port: int, t: str):
        # MQTT Up and Running
        self.client = mqtt.Client()
        self.client.connect(mqtt_ip, mqtt_port)
        self.client.on_connect = self._on_connect
        self.message_callback_add('I1820/%s/event' % t, self._on_notification)

        # API Token
        self.token = t

        # IoT Things
        self.things = []

        # Notification handlers
        self.notification_handlers = {}

    def add_thing(self, type, id, attributes={}):
        self.things.append({'type': type, 'id': id, 'attributes': attributes})

    def run(self):
        print(" * Node ID: %s" % i1820_id)
        PingService(self.base_url, self.things).ping()
        self.client.loop_start()

    def notification(self, thing: str):
        def _notification(fn):
            self.notification_handlers[thing] = fn
            return fn
        return _notification

    def log(self, type, device, states):
        log = I1820Log(type, device, states, str(i1820_id))
        self.client.publish('I1820/%s/log' % self.token, bson.dumps(log))

    def _on_notification(self, client, userdata, message):
        notif = bson.loads(message.payload)

        if not isinstance(notif, I1820Notification):
            return

        if notif.endpoint != self.i1820_id:
            return

        try:
            self.notification_handlers[notif.type](notif)
        except KeyError:
            pass
