#!/usr/bin/env python3

from I1820.app import I1820App
from I1820.domain.notif import I1820Notification

import time

token = '83DB8F6299E0A303730B5F913B6A3DF420EBC2C2'

app = I1820App(token, '192.168.1.19')


@app.notification('lamp')
def lamp_notification(data: I1820Notification):
    print(data)

if __name__ == '__main__':
    app.add_thing('lamp', '1:1')
    app.add_thing('current', '1')
    app.run()
    i = 10
    while True:
        i = (i + 10) % 100
        app.log('current', '1', {'current': str(i)})
        time.sleep(10)
