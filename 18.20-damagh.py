#!/usr/bin/env python3
import serial

from I1820.app import I1820App
# from I1820.domain.notif import I1820Notification

tenant_id = 'aolab'

app = I1820App(tenant_id, 'iot.ceit.aut.ac.ir', 58904)

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=9600, timeout=1)

line = []


def serial_read():
    global line
    line.append(ser.read())
    if len(line) > 1 and line[-1] == b'\n':
        line = line[:-2]
        line = b''.join(line).decode('ascii')
        t = float(line)
        app.log('temperature', 'Honeyeh',
                [{'name': 'temperature', 'value': t}])
        line = []


if __name__ == '__main__':
    # temperature
    app.add_thing('temperature', 'Honeyeh')

    app.run()
    while True:
        try:
            serial_read()
        except Exception as e:
            pass
