#!/usr/bin/env python3
import serial

from xbee import ZigBee
from I1820.app import I1820App
from I1820.domain.notif import I1820Notification

token = '4b565730-a4b1-11e6-8c5a-7f854f832032'
app = I1820App(token, 'iot.ceit.aut.ac.ir', 58904)

serial_port = serial.Serial('/dev/ttyUSB0', 9600)
xbee = ZigBee(serial_port)


@app.notification('lamp')
def led_notification(data: I1820Notification):
    # device_id = data.device
    command = b'\x05' if data.settings['on'] else b'\x04'
    xbee.remote_at(dest_addr_long=b'\x00\x13\xa2\x00@\xe47',
                   command=b'D1', parameter=command)


if __name__ == '__main__':
    app.add_thing('lamp', '\x00\x13\xa2\x00@\xe47')
    app.add_thing('multisensor', '1')
    app.run()
    while True:
        frame = xbee.wait_read_frame()
        print(frame)
        sample = frame['samples'][0]
        if (len(sample.keys()) == 4):
            humidity = str((sample['adc-2'] - 500) / 5)
            temperature = str(sample['adc-1'] + 20)
            temperature = temperature[:2] + '.' + temperature[2:]
            light = str(sample['adc-0'])
            app.log('multisensor', '1', {'humidity': humidity,
                                         'temperature': temperature,
                                         'light': light}
                    )
