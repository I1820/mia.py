#!/usr/bin/env python3
import serial
import io

from I1820.app import I1820App
from I1820.domain.notif import I1820Notification

tenant_id = 'aolab'

app = I1820App(tenant_id, 'iot.ceit.aut.ac.ir', 58904)

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=9600, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))


def serial_read():
    line = sio.readline()
    if len(line) > 1:
        t_id = line[0]
        line = line[2:]
        t = float(line)
        print("%s: %g" % (t_id, t))
        app.log('temperature', 'Honeyeh-%s' % t_id,
                [{'name': 'temperature', 'value': t}])


@app.notification('alarm')
def alarm_notification(data: I1820Notification):
    for setting in data.settings:
        if setting['name'] == 'on':
            if setting['value']:
                command = 'E'
            else:
                command = 'D'

    sio.write(command + '\n\r')
    sio.flush()


if __name__ == '__main__':
    # temperature
    app.add_thing('temperature', 'Honeyeh-1')
    app.add_thing('temperature', 'Honeyeh-2')
    app.add_thing('alarm', 'Honeyeh-3')

    app.run()
    while True:
        try:
            sio.flush()
            serial_read()
        except Exception as e:
            pass
