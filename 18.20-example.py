#!/usr/bin/env python3

from I1820.app import I1820App

import time


app = I1820App('192.168.1.9', 1373)


@app.notification('lamp')
def lamp_notification(data: dict):
    print(data)

if __name__ == '__main__':
    app.add_thing('lamp', '0')
    app.add_thing('temperature', '1')
    app.start()
    i = 10
    while True:
        i = (i + 10) % 100
        app.log('temperature', '1', {'temperature': i})
        time.sleep(10)
