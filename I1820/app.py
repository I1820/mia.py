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

i1820_logger_app = logging.getLogger('I1820.app')


class I1820App:
    def __init__(self, tenant_id: str, mqtt_ip: str, mqtt_port: int=1883,
                 logger=None):
        # MQTT Up and Running
        self.client = mqtt.Client()
        self.client.connect(mqtt_ip, mqtt_port)
        self.client.on_connect = self._on_connect

        # Tenant Identification
        self.tenant_id = tenant_id

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
        self._ping()
        self.client.loop_start()

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
        self.client.publish('I1820/%s/log/send' % self.tenant_id,
                            log.to_json())

    def _ping(self):
        self.client.publish('I1820/%s/discovery/ping' % self.tenant_id,
                            self.agent.to_json())
        t = threading.Timer(10, self._ping)
        t.daemon = True
        t.start()

    def _on_connect(self, client, userdata, flags, rc):
        client.subscribe('I1820/%s/notification' % self.tenant_id)
        client.message_callback_add('I1820/%s/notification' % self.tenant_id,
                                    self._on_notification)
        client.subscribe('I1820/%s/action' % self.tenant_id)
        client.message_callback_add('I1820/%s/action' % self.tenant_id,
                                    self._on_action)

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
