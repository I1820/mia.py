#!/usr/bin/env python3
import serial
from xbee import ZigBee
from I1820.app import I1820App

app = I1820App('192.168.128.90', 8080, '0.0.0.0', 1820)


if __name__ == '__main__':
    serial_port = serial.Serial('/dev/ttyUSB1', 9600)
    xbee = ZigBee(serial_port)
    app.add_thing('multisensor', '1')
    app.start()
    while True:
        frame = xbee.wait_read_frame()
        print(frame)
        sample = frame['samples'][0]
        humidity = str(sample['adc-2'])
        temperature = str(sample['adc-1'])
        light = str(sample['adc-0'])
        app.log('multisensor', '1', {'humidity': humidity,
                                     'temperature': temperature,
                                     'light': light}
                )
