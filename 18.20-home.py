#!/usr/bin/env python3
import serial
import io
import logging

from AoLab.protocol.hasht import HashtProtocol
from I1820.app import I1820App
from I1820.domain.notif import I1820Notification


token = '83DB8F6299E0A303730B5F913B6A3DF420EBC2C2'

app = I1820App(token, '192.168.1.19')


ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=115200, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

logger = logging.getLogger('I1820.home')


@app.notification('lamp')
def lamp_notification(data: I1820Notification):
    print(data)
    node_id, device_id = data.device.split(':')
    if 'on' in data.settings:
        command = '1' if data.settings['on'] else '0'
    else:
        return

    command_raw = HashtProtocol().marshal(data.type, device_id,
                                          node_id, command)

    serial_write(command_raw)


@app.notification('cooler')
def cooler_notification(data: I1820Notification):
    node_id, device_id = data.device.split(':')
    if 'on' in data.settings:
        command = '1' if data.settings['on'] else '0'
    elif 'temperature' in data.settings:
        command = str(data.settings['temperature'])
    else:
        return

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
        states = {}
        for thing in data.things:
            states[thing['type']] = thing['value']
        states['battery'] = data.battery
        app.log('multisensor', data.node_id, states)

if __name__ == '__main__':
    # MultiSensors
    app.add_thing('multisensor', '2')

    # Coolers
    app.add_thing('cooler', '1:1')

    # Lamps
    for i in range(1, 10):
        app.add_thing('lamp', '%d:%d' % (1, i))

    app.run()
    while True:
        serial_read()
