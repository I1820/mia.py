#!/usr/bin/env python3
import serial
import io
import time

from AoLab.protocol.hasht import HashtProtocol
from I1820.app import I1820App
from I1820.domain.notif import I1820Notification

app = I1820App('192.168.128.90', 8080, '0.0.0.0', 1820)

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=9600, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))


@app.notification('lamp')
def send_notification(data: I1820Notification):
    node_id, device_id = data.device_id.split(':')
    command = '1' if data.settings['on'] else '0'

    time.sleep(5)
    sio.write(HashtProtocol().marshal(data.type, device_id,
                                      node_id, command))
    sio.flush()
    ser.flush()

if __name__ == '__main__':
    # MultiSensors
    app.add_thing('multisensor', '1')
    app.add_thing('multisensor', '2')
    app.add_thing('multisensor', '3')
    app.add_thing('multisensor', '4')

    # Lamp
    app.add_thing('lamp', '1:2')

    app.start()
    while True:
        line = sio.readline()
        print(line)
        data = HashtProtocol().unmarshal(line)
        if data is not None:
            states = {}
            for thing in data.things:
                states[thing['type']] = thing['value']
            app.log('multisensor', data.node_id, states)
