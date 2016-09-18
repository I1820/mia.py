#!/usr/bin/env python3
import serial
import io

from AoLab.protocol.hasht import HashtProtocol
from I1820.app import I1820App

app = I1820App('127.0.0.1', 1373, '0.0.0.0', 3000)


if __name__ == '__main__':
    app.add_thing('temperature', '0')
    app.start()
    ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=9600, timeout=1)
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

    while True:
        line = sio.readline()
        data = HashtProtocol().handler(line)
        if data is not None:
            for thing in data.things:
                app.log(thing['type'],
                        "%s:%s" % (data.node_id, thing['device']),
                        {thing['type']: thing['value']})
