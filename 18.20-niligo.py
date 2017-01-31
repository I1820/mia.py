#!/usr/bin/env python3
import logging
import requests

from netdisco.discovery import NetworkDiscovery
from I1820.app import I1820App
from I1820.domain.notif import I1820Notification


token = '83DB8F6299E0A303730B5F913B6A3DF420EBC2C2'

app = I1820App(token, 'iot.ceit.aut.ac.ir', 58904)

logger = logging.getLogger('I1820.niligo')


@app.notification('smartLamp')
def itunes_notification(data: I1820Notification):
    for setting in data.settings:
        if setting['name'] == 'on':
            if setting['value']:
                requests.get('http://<ip>/api/state?power=1')
            else:
                requests.get('http://<ip>/api/state?power=0')

if __name__ == '__main__':
    netdis = NetworkDiscovery()

    netdis.scan()

    for dev in netdis.discover():
        print(dev, netdis.get_info(dev))

        netdis.stop()

    app.add_thing('smartLamp', '1')

    app.run()
    while True:
        pass
