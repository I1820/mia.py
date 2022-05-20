#!/usr/bin/env python3

from I1820.app import I1820App
from I1820.domain.notif import I1820Notification


token = '83DB8F6299E0A303730B5F913B6A3DF420EBC2C2'

app = I1820App(token, 'iot.ceit.aut.ac.ir', 58904)


@app.notification('lamp')
def lamp_notification(data: I1820Notification):
    print(data)

if __name__ == '__main__':
    app.add_thing('lamp', '1:1')
    app.add_thing('temperature', '1')
    app.run()
    while True:
        pass
