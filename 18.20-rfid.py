#!/usr/bin/env python3
import serial
import io
import logging
import time
import RPi.GPIO as GPIO

from I1820.app import I1820App
from I1820.domain.notif import I1820Notification

token = '83DB8F6299E0A303730B5F913B6A3DF420EBC2C2'

app = I1820App(token, '192.168.1.19')

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=9600, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

logger = logging.getLogger('I1820.rfid')

uid_storage = {}

@app.notification('lamp')
def lamp_notification(data: I1820Notification):
    if 'on' in data.settings:
        if data.settings['on']:
            GPIO.output(24, True)
        else:
            GPIO.output(24, False)
    else:
        return


def serial_read():
    line = sio.readline()
    if len(line) != 0 and line[0] == '@':
        uid = line[2:-1]
        if uid not in uid_storage:
            uid_storage[uid] = 'Unknown'
        logger.info("UID: %s" % uid)
        app.log('rfid', '1', {'uid': uid, 'name': uid_storage[uid]})

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(24, GPIO.OUT)

    # RFID
    app.add_thing('rfid', '1')

    # Lamp
    app.add_thing('lamp', '1')

    app.run()
    while True:
        try:
            serial_read()
        except Exception as e:
            logger.error(e)
            pass
