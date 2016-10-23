#!/usr/bin/env python3
import time

from I1820.app import I1820App
from I1820.domain.notif import I1820Notification


token = '1c7159b0-9570-11e6-88f5-09fddd50ddda'

app = I1820App(token, 'iot.ceit.aut.ac.ir', 58904)


@app.notification('lamp')
def lamp_notification(data: I1820Notification):
    print(data)

if __name__ == '__main__':
    app.add_thing('lamp', '1:1')
    app.add_thing('temperature', '1')
    app.run()
    i = 10
    while True:
        i = (i + 10) % 100
        app.log('temperature', '1', {'temperature': str(i)})
        time.sleep(10)
