#!/usr/bin/env python3
import serial

from xbee import ZigBee
from I1820.app import I1820App
from I1820.domain.notif import I1820Notification

token = '83DB8F6299E0A303730B5F913B6A3DF420EBC2C2'
app = I1820App(token, 'iot.ceit.aut.ac.ir', 58904)

serial_port = serial.Serial('/dev/ttyUSB0', 9600)
xbee = ZigBee(serial_port)


@app.notification('lamp')
def led_notification(data: I1820Notification):
    node_id, device_id = data.device.split(':')

    node_id = b'\x00\x13\xa2\x00@\xe47-'
    device_id = device_id.encode('utf-8')

    command = b'\x04' if data.settings['on'] else b'\x05'

    xbee.remote_at(dest_addr_long=node_id,
                   command=b'D%s' % device_id,
                   parameter=command)


def turnoff():
    command = b'\x05'
    for device in [b'D0', b'D1', b'D2']:
        xbee.remote_at(dest_addr_long=b'\x00\x13\xa2\x00@\xe47-',
                       command=device, parameter=command)

if __name__ == '__main__':
    turnoff()
    app.add_thing('lamp', '\x00\x13\xa2\x00@\xe47-:0')
    app.add_thing('lamp', '\x00\x13\xa2\x00@\xe47-:1')
    app.add_thing('lamp', '\x00\x13\xa2\x00@\xe47-:2')
    app.add_thing('multisensor', '1')
    app.run()
    while True:
        frame = xbee.wait_read_frame()
        print(frame)
        sample = frame['samples'][0]
        for key in sample:
            if key == 'adc-2':
                humidity = str((sample['adc-2'] - 500) / 5)
                app.log('multisensor', '1', {'humidity': humidity})
            elif key == 'adc-1':
                temperature = str(sample['adc-1'] + 20)
                app.log('multisensor', '1', {'temperature': temperature})
            elif key == 'adc-0':
                light = str(sample['adc-0'])
                app.log('multisensor', '1', {'light': light})
