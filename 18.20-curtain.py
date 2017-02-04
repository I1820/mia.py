#!/usr/bin/env python3
import serial
import io
import logging

from AoLab.protocol.hasht import HashtProtocol
from I1820.app import I1820App
from I1820.domain.notif import I1820Notification

token = '83DB8F6299E0A303730B5F913B6A3DF420EBC2C2'

app = I1820App(token, '127.0.0.1')

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=115200, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

logger = logging.getLogger('I1820.curtain')


@app.notification('curtain')
def curtain_notification(data: I1820Notification):
    node_id, device_id = data.device.split(':')
    for setting in data.settings:
        if setting['name'] == 'height':
            command = str(setting['value'])

    command_raw = HashtProtocol().marshal(data.type, device_id,
                                          node_id, command)

    serial_write(command_raw)


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
    # Curtain
    app.add_thing('curtain', '3:2')

    app.run()
    while True:
        try:
            serial_read()
        except Exception as e:
            logger.error(str(e))
            pass
