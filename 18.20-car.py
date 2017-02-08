#!/usr/bin/env python3
import serial
import io
import logging

from I1820.app import I1820App

token = '83DB8F6299E0A303730B5F913B6A3DF420EBC2C2'

app = I1820App(token, 'iot.ceit.aut.ac.ir', 58904)

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=9600, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

logger = logging.getLogger('I1820.car')

line = []


def serial_read():
    global line
    line.append(ser.read())
    if len(line) > 1 and line[-1] == b'\n':
        a = int(line[-3])
        if line[-4] == b'-':
            a = -a
        logger.info("a: %s" % a)
        app.log('accelerometer', '1', [{'name': 'accelerate', 'value': a}])
        line = []


if __name__ == '__main__':
    # accelerometer
    app.add_thing('accelerometer', '1')

    app.run()
    while True:
        try:
            serial_read()
        except Exception as e:
            logger.error(e)
            pass
