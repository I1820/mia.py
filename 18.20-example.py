#!/usr/bin/env python3

from I1820.app import I1820App
from I1820.domain.notif import I1820Notification

import time

token = '83DB8F6299E0A303730B5F913B6A3DF420EBC2C2'

app = I1820App(token, '192.168.1.19')


@app.notification('lamp', 'alarm')
def lamp_notification(data: I1820Notification):
    pass


if __name__ == '__main__':
    app.add_thing('lamp', '1:1')
    app.add_thing('alarm', '1:2')
    app.add_thing('multisensor', '1')
    app.run()
    t = 10
    l = 1024
    m = 1
    while True:
        t = (t + 10) % 100
        l = l / 2 if l >= 128 else l * 2
        m = 0 if m == 1 else 1

        states = []
        states.append({
            'name': 'temperature',
            'value': str(t)
        })
        states.append({
            'name': 'light',
            'value': str(l)
        })
        states.append({
            'name': 'motion',
            'value': str(m)
        })
        states.append({
            'name': 'humidity',
            'value': '24'
        })

        app.log('multisensor', '1', states)
        time.sleep(5)
