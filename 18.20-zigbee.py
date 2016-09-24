#!/usr/bin/env python3
import serial

from xbee import ZigBee
from I1820.app import I1820App
from I1820.domain.notif import I1820Notification

app = I1820App('192.168.128.90', 8080, '0.0.0.0', 1820)

serial_port = serial.Serial('/dev/ttyUSB0', 9600)
xbee = ZigBee(serial_port)


@app.notification('lamp')
def led_notification(data: I1820Notification):
    device_id = data.device
    command = b'\x05' if data.settings['on'] else b'\x04'
    xbee.remote_at(dest_addr_long=device_id, command=b'D1', parameter=command)


if __name__ == '__main__':
    app.add_thing('lamp', '\x00\x13\xa2\x00@\xc1\xa9o')
    app.add_thing('multisensor', '1')
    app.start()
    while True:
        frame = xbee.wait_read_frame()
        print(frame)
        sample = frame['samples'][0]
        if (len(sample.keys()) == 4):
            humidity = str(sample['adc-2'])
            temperature = str(sample['adc-1'])
            light = str(sample['adc-0'])
            app.log('multisensor', '1', {'humidity': humidity,
                                         'temperature': temperature,
                                         'light': light}
                    )
