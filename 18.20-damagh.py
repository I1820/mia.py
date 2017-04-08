#!/usr/bin/env python3
import serial

from I1820.app import I1820App
from I1820.domain.notif import I1820Notification

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
        t_id = line[0]
        line = line[2:]
        t = float(line)
        print(t)
        app.log('temperature', 'Honeyeh-%s' % t_id,
                [{'name': 'temperature', 'value': t}])
        line = []


@app.notification('alarm')
def alarm_notification(data: I1820Notification):
    for setting in data.settings:
        if setting['name'] == 'on':
            if setting['value']:
                command = 'E'
            else:
                command = 'D'

    ser.write(command.encode('ascii'))
    ser.flush()


if __name__ == '__main__':
    # temperature
    app.add_thing('temperature', 'Honeyeh-1')
    app.add_thing('temperature', 'Honeyeh-2')
    app.add_thing('alarm', 'Honeyeh-3')

    app.run()
    while True:
        try:
            serial_read()
        except Exception as e:
            pass
