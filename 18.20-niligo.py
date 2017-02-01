#!/usr/bin/env python3
import requests
from requests.auth import HTTPDigestAuth

from I1820.app import I1820App
from I1820.domain.notif import I1820Notification

token = '83DB8F6299E0A303730B5F913B6A3DF420EBC2C2'

app = I1820App(token, '127.0.0.1')
url = 'http://192.168.100.1/api/state'
session = requests.Session()
session.auth = HTTPDigestAuth('admin', 'admin')


@app.notification('smartLamp')
def notif(jnotif: I1820Notification):
    for setting in jnotif.settings:
        if setting['name'] == 'on' :
            if setting['value']:
                post_data = {'power': '1'}
                for i in range(3):
                    try:
                        session.get(url, params=post_data, verify=False)
                    except Exception:
                        pass
            else:
                post_data = {'power': '0'}
                for i in range(3):
                    try:
                        session.get(url, params=post_data, verify=False)
                    except Exception:
                        pass
        elif setting['name']=='color':
            post_data = {'color':setting['value'][1:]}
            for i in range(3):
                try:
                    session.get(url, params=post_data, verify=False)
                except Exception:
                    pass
        elif setting['name'] == 'fade':
            post_data = {'fade': setting['value'][:-1]}
            for i in range(3):
                session.get(url, params=post_data, verify=False)

if __name__ == '__main__':
    app.add_thing('smartLamp', '1')
    app.run()
    while True:
        pass
