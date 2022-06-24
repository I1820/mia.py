import logging
import threading
import time

import paho.mqtt.client as mqtt

from . import i1820_id
from .domain.agent import I1820Agent
from .domain.log import I1820Log
from .domain.notif import I1820Notification


class I1820App:
    def __init__(self, tenant_id: str, mqtt_ip: str, mqtt_port: int = 1883):
        # MQTT Up and Running
        self.client = mqtt.Client()
        self.client.reconnect_delay_set(1, 360)
        self.client.connect(mqtt_ip, mqtt_port)
        self.client.on_connect = self._on_connect

        # Tenant Identification
        self.tenant_id = tenant_id

        # I1829 Agent
        self.agent = I1820Agent(str(i1820_id), [])

        # Notification/Action handlers
        self.notification_handlers = {}
        self.action_handlers = {}

        self.logger = logging.getLogger("I1820.app")

    def add_thing(self, device_type: str, device_id: str):
        self.agent.things.append({"type": device_type, "id": device_id})

    def run(self):
        print(f" * Node ID: {i1820_id}")
        threading.Thread(
            target=self._ping,
            name="ping_thread",
            daemon=True,
        ).start()
        threading.Thread(
            target=self.client.loop_forever,
            name="mqtt_thread",
            daemon=True,
            kwargs={'retry_first_connection': True}
        ).start()

    def notification(self, *things: str):
        def _notification(func):
            for thing in things:
                self.notification_handlers[thing] = func
            return func

        return _notification

    def log(self, device_type: str, device_id: str, states):
        log = I1820Log(device_type, device_id, states, str(i1820_id))
        self.client.publish(f"I1820/{self.tenant_id}/log/send", log.to_json())

    def _ping(self):
        while True:
            self.client.publish(
                f"I1820/{self.tenant_id}/agent/ping", self.agent.to_json()
            )
            # sleeps for 10 seconds
            time.sleep(10)

    def _on_connect(self, client, userdata, flags, rc):
        print(" * MQTT connection is up and running")
        client.subscribe(f"I1820/{self.tenant_id}/configuration/request")
        client.message_callback_add(
            f"I1820/{self.tenant_id}/configuration/request",
            self._on_notification,
        )

    def _on_notification(self, client, userdata, message):
        notif = I1820Notification.from_json(message.payload.decode("ascii"))

        if notif.agent != str(i1820_id):
            return

        try:
            ret = self.notification_handlers[notif.type](notif)
            if ret is True:
                client.publish(
                    "I1820/%s/configuration/change" % self.tenant_id,
                    notif.to_json(),
                )
            self.logger.info(
                "device: %s -- settings: %r" % (notif.device, notif.settings)
            )
        except KeyError:
            pass
