#!/usr/bin/env python3
import serial
from xbee import ZigBee
from I1820.app import I1820App
from I1820.log.log import I1820Log

app = I1820App('192.168.1.9', 1373)

app.add_thing('temprature', '0')

if __name__ == '__main__':
    serial_port = serial.Serial('COM3', 9600)
    xbee = ZigBee(serial_port)
    app.start()
    while True:
        frame = xbee.wait_read_frame()
        log = I1820Log()
        app.log(log)
