#!/usr/bin/env python3
import serial
import io

from AoLab.protocol.hasht import HashtProtocol
from I1820.app import I1820App
from I1820.domain.notif import I1820Notification

app = I1820App('192.168.128.90', 8080, '0.0.0.0', 1820)

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=9600, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))


@app.notification('lamp')
def lamp_notification(data: I1820Notification):
    node_id, device_id = data.device.split(':')
    command = '1' if data.settings['on'] else '0'

    command_raw = HashtProtocol().marshal(data.type, device_id,
                                          node_id, command)

    serial_write(command_raw)


@app.notification('cooler')
def cooler_notification(data: I1820Notification):
    node_id, device_id = data.device.split(':')
    command = '1' if data.settings['on'] else '0'

    command_raw = HashtProtocol().marshal(data.type, device_id,
                                          node_id, command)

    serial_write(command_raw)


def serial_write(command):
    sio.write(command)
    sio.flush()


def serial_read():
    line = sio.readline()
    if len(line) != 0:
        print(line)
    data = HashtProtocol().unmarshal(line)
    if data is not None:
        states = {}
        for thing in data.things:
            states[thing['type']] = thing['value']
        app.log('multisensor', data.node_id, states)

if __name__ == '__main__':
    # MultiSensors
    app.add_thing('multisensor', '1')
    app.add_thing('multisensor', '2')
    app.add_thing('multisensor', '3')
    app.add_thing('multisensor', '4')
    app.add_thing('multisensor', '5')
    app.add_thing('multisensor', '6')
    app.add_thing('multisensor', '7')

    # Lamp
    for i in range(1, 10):
        for j in range(1, 3):
            app.add_thing('lamp', '%d:%d' % (j, i))

    app.start()
    while True:
        serial_read()
