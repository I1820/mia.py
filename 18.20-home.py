#!/usr/bin/env python3
import logging
import requests
import io
import serial
import sys


from I1820.app import I1820App
from I1820.domain.notif import I1820Notification
from AoLab.protocol.hasht import HashtProtocol


token = 'parham-home'

app = I1820App(token, '192.168.1.19')

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=115200, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

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


def serial_write(command):
    sio.write(command)
    sio.flush()


def serial_read():
    line = sio.readline()
    if len(line) != 0:
        logger.info(line)
    data = HashtProtocol().unmarshal(line)
    if data is not None:
        states = []
        for thing in data.things:
            states.append({
                'name': thing['type'],
                'value': thing['value']
            })
        if data.battery != 0:
            states.append({'name': 'battery',
                          'value': data.battery})
        if data.node_id != '9':
            app.log('multisensor', data.node_id, states)
        else:
            app.log('gas', data.node_id, states)


if __name__ == '__main__':
    app.add_thing('itunes', '1')
    app.add_thing('multisensor', '6')

    app.run()
    while True:
        try:
            serial_read()
        except serial.SerialException:
            sys.exit(1)
        except Exception as e:
            logger.error(str(e))
