#!/usr/bin/env python3
import logging
import requests

from I1820.app import I1820App
from I1820.domain.notif import I1820Notification


token = '83DB8F6299E0A303730B5F913B6A3DF420EBC2C2'

app = I1820App(token, '192.168.1.19')


logger = logging.getLogger('I1820.home')


@app.notification('itunes')
def itunes_notification(data: I1820Notification):
    for setting in data.settings:
        if setting['name'] == 'play':
            if setting['value']:
                requests.put('http://192.168.1.2:8181/play')
            else:
                requests.put('http://192.168.1.2:8181/pause')
        if setting['name'] == 'direction':
            if setting['value']:
                requests.put('http://192.168.1.2:8181/next')
            else:
                requests.put('http://192.168.1.2:8181/previous')


if __name__ == '__main__':
    app.add_thing('itunes', '1')

    app.run()
    while True:
        pass
