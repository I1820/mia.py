#!/usr/bin/env python3
import serial
import io
import logging

from I1820.app import I1820App
from I1820.domain.notif import I1820Notification

token = '83DB8F6299E0A303730B5F913B6A3DF420EBC2C2'

app = I1820App(token, 'iot.ceit.aut.ac.ir', 58904)

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=9600, timeout=1)

line = []


def serial_read():
    global line
    line.append(ser.read())
    if len(line) > 1 and line[-1] == b'\n':
        line = line[:-3]
        sline = b''.join(line).decode('ascii')
        sline, a = sline.rsplit('$', maxsplit=1)
        a = float(a)
        id = sline[-14:]
        print("Zigbee id: %s, %g" % (id, a))
        app.log('accelerometer', '1', [{'name': 'accelerate', 'value': str(a)}])
        line = []


@app.notification('alarm')
def lamp_notification(data: I1820Notification):
    for setting in data.settings:
        if setting['name'] == 'on':
            command = 'Traffic' if setting['value'] else 'Normal'

    ser.write(command.encode('ascii'))
    ser.flush()


if __name__ == '__main__':
    # accelerometer
    app.add_thing('accelerometer', '1')
    app.add_thing('alarm', '1')

    app.run()
    while True:
        try:
            serial_read()
        except Exception as e:
            pass
