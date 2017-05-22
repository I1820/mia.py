#!/usr/bin/env python3
import serial
import io
import logging
import time
import sys

from AoLab.protocol.hasht import HashtProtocol
from I1820.app import I1820App
from I1820.domain.notif import I1820Notification

tenant_id = 'aolab'

app = I1820App(tenant_id, 'iot.ceit.aut.ac.ir', 58904)

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=115200, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

logger = logging.getLogger('I1820.aolab')


@app.notification('lamp', 'alarm')
def lamp_notification(data: I1820Notification):
    time.sleep(0.01)
    node_id, device_id = data.device.split(':')

    for setting in data.settings:
        if setting['name'] == 'on':
            command = '1' if setting['value'] else '0'

    command_raw = HashtProtocol().marshal(data.type, device_id,
                                          node_id, command)

    serial_write(command_raw)


@app.notification('cooler')
def cooler_notification(data: I1820Notification):
    node_id, device_id = data.device.split(':')

    for setting in data.settings:
        if setting['name'] == 'on':
            command = '11' if setting['value'] else '0'
        elif setting.name == 'temperature':
            command = str(setting.value)

    command_raw = HashtProtocol().marshal(data.type, device_id,
                                          node_id, command)

    serial_write(command_raw)


@app.notification('curtain')
def curtain_notification(data: I1820Notification):
    node_id, device_id = data.device.split(':')
    for setting in data.settings:
        if setting['name'] == 'height':
            command = str(setting['value'])

    command_raw = HashtProtocol().marshal(data.type, device_id,
                                          node_id, command)

    serial_write(command_raw)


@app.notification('projector')
def curtain_notification(data: I1820Notification):
    node_id, device_id = data.device.split(':')
    for setting in data.settings:
        if setting['name'] == 'on':
            command = '2'
        if setting['name'] == 'input':
            command = '3'

    command_raw = HashtProtocol().marshal(data.type, device_id,
                                          node_id, command)

    serial_write(command_raw)


@app.notification('tv')
def curtain_notification(data: I1820Notification):
    node_id, device_id = data.device.split(':')
    for setting in data.settings:
        if setting['name'] == 'on':
            command = '4'

    command_raw = HashtProtocol().marshal(data.type, device_id,
                                          node_id, command)

    serial_write(command_raw)

@app.notification('mode')
def curtain_notification(data: I1820Notification):
    if data.device == 'presentation':
        for setting in data.settings:
            if setting['name'] == 'on':
                if setting['value']:
                    command = '@1,p2.@2,l70.@2,l80.@2,l90.@3,l70.@3,l80.@3,l90.@4,p1-260.'
                else:
                    command = '@1,p2.@2,l71.@2,l81.@2,l91.@1,p2.@3,l71.@3,l81.@3,l91.@4,p1+260.'
        serial_write(command)


def serial_write(command):
    sio.write(command)
    sio.flush()


def serial_read():
    line = sio.readline()
    if len(line) != 0:
        logger.info(line)
    data = HashtProtocol().unmarshal(line)
    if data is not None:
        states = []
        for thing in data.things:
            states.append({
                'name': thing['type'],
                'value': thing['value']
            })
        if data.battery != 0:
            states.append({'name': 'battery',
                          'value': data.battery})
        if data.node_id != '9':
            app.log('multisensor', data.node_id, states)
        else:
            app.log('gas', data.node_id, states)


if __name__ == '__main__':
    # MultiSensors
    app.add_thing('multisensor', '5')
    app.add_thing('multisensor', '6')
    app.add_thing('multisensor', '1')
    app.add_thing('multisensor', '8')
    app.add_thing('gas', '9')

    # Lamps
    for i in range(1, 10):
        app.add_thing('lamp', '2:%d' % i)
        app.add_thing('lamp', '3:%d' % i)

    app.add_thing('cooler', '1:1')
    app.add_thing('curtain', '4:1')
    app.add_thing('projector', '1:1')
    app.add_thing('tv', '1:1')
    app.add_thing('mode', 'presentation')

    app.run()
    while True:
        try:
            serial_read()
        except serial.SerialException:
            sys.exit(1)
        except Exception as e:
            logger.error(str(e))
