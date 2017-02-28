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
from .domain.agent import I1820Agent
from . import i1820_id

import paho.mqtt.client as mqtt
import threading
import logging
import json
import time

i1820_logger_app = logging.getLogger('I1820.app')


class I1820App:
    def __init__(self, mqtt_ip: str, mqtt_port: int=1883,
                 logger=None):
        # MQTT Up and Running
        self.client = mqtt.Client()
        self.client.connect(mqtt_ip, mqtt_port)
        self.client.on_connect = self._on_connect

        # API Token
        self.token = None

        # I1829 Agent
        self.agent = I1820Agent(str(i1820_id), [])

        # Notification/Action handlers
        self.notification_handlers = {}
        self.action_handlers = {}

        if logger is None:
            self.logger = i1820_logger_app

    def add_thing(self, type, id):
        self.agent.things.append({'type': type, 'id': id})

    def run(self):
        print(" * Node ID: %s" % i1820_id)
        self.client.loop_start()
        print(" * Waiting for I1820 ...")
        while self.token is None:
            self.client.publish('I1820/discovery', self.agent.to_json())
            time.sleep(1.5)
        print(" * I1820 Master: %s" % self.token)
        self._ping()

    def notification(self, *things: [str]):
        def _notification(fn):
            for thing in things:
                self.notification_handlers[thing] = fn
            return fn
        return _notification

    def action(self, *names: [str]):
        def _action(fn):
            for name in names:
                self.action_handlers[name] = fn
            return fn
        return _action

    def log(self, type, device, states):
        log = I1820Log(type, device, states, str(i1820_id))
        self.client.publish('I1820/%s/log' % self.token, log.to_json())

    def _on_discovery_ack(self, client, userdata, message):
        resp = json.loads(message.payload.decode('ascii'))
        if resp['id'] != str(i1820_id):
            return
        self.token = resp['master']
        client.unsubscribe('I1820/discovery-ack')
        client.subscribe('I1820/%s/notification' % self.token)
        client.message_callback_add('I1820/%s/notification' % self.token,
                                    self._on_notification)
        client.message_callback_add('I1820/%s/action' % self.token,
                                    self._on_action)

    def _ping(self):
        self.client.publish('I1820/%s/discovery' % self.token,
                            self.agent.to_json())
        t = threading.Timer(10, self._ping)
        t.daemon = True
        t.start()

    def _on_connect(self, client, userdata, flags, rc):
        client.subscribe('I1820/discovery-ack')
        client.message_callback_add('I1820/discovery-ack', self._on_discovery_ack)

    def _on_action(self, client, userdata, message):
        pass

    def _on_notification(self, client, userdata, message):
        notif = I1820Notification.from_json(message.payload.decode('ascii'))

        if notif.agent != str(i1820_id):
            return

        try:
            self.notification_handlers[notif.type](notif)
            self.logger.info('device: %s -- settings: %r' %
                             (notif.device, notif.settings))
        except KeyError:
            pass
