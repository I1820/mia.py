#!/usr/bin/env python3

import time
from datetime import datetime

from mia_py.I1820.app import I1820App
from mia_py.I1820.domain.notif import I1820Notification

tenant_id = "parham-home"

app = I1820App(tenant_id, "127.0.0.1")


@app.notification("lamp", "alarm", "smartLamp")
def lamp_notification(data: I1820Notification):
    return True


if __name__ == "__main__":
    app.add_thing("lamp", "1:1")
    app.add_thing("alarm", "1:2")
    app.add_thing("smartLamp", "1:3")
    app.add_thing("multisensor", "1")

    app.run()

    TEMPERATURE = 10
    LIGHT = 1024
    MOTION = 1
    while True:
        TEMPERATURE = (TEMPERATURE + 10) % 100
        LIGHT = LIGHT / 2 if LIGHT >= 128 else LIGHT * 2
        MOTION = 0 if MOTION == 1 else 1

        states = []
        states.append({"name": "temperature", "value": str(TEMPERATURE)})
        states.append({"name": "light", "value": str(LIGHT)})
        states.append({"name": "motion", "value": str(MOTION)})
        states.append({"name": "humidity", "value": "24"})

        app.log("multisensor", "1", states)
        print(f'sending information to mia {datetime.now()}')
        time.sleep(5)
