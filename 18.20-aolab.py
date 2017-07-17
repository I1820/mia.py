#!/usr/bin/env python3
import serial
import io
import logging
import time

from AoLab.protocol.hasht import HashtProtocol
from I1820.app import I1820App
from I1820.domain.notif import I1820Notification

tenant_id = 'aolab'

app = I1820App(tenant_id, 'iot.ceit.aut.ac.ir', 58904)

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=115200, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

logger = logging.getLogger('I1820.aolab')

alarm_is_on = False
fire_scenario = True


@app.notification('lamp', 'alarm', 'valve')
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
        elif setting['name'] == 'temperature':
            command = str(setting['value'])

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
def projector_notification(data: I1820Notification):
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
def tv_notification(data: I1820Notification):
    node_id, device_id = data.device.split(':')
    for setting in data.settings:
        if setting['name'] == 'on':
            command = '4'

    command_raw = HashtProtocol().marshal(data.type, device_id,
                                          node_id, command)

    serial_write(command_raw)


@app.notification('mode')
def mode_notification(data: I1820Notification):
    global fire_scenario
    global alarm_is_on
    if data.device == 'fire':
        for setting in data.settings:
            if setting['name'] == 'on':
                if setting['value']:
                    fire_scenario = True
                    command = '-'
                    alarm_is_on = False
                else:
                    fire_scenario = False
                    command = '@5,A30.'
                    alarm_is_on = False
        serial_write(command)
    if data.device == 'presentation':
        for setting in data.settings:
            if setting['name'] == 'on':
                if setting['value']:
                    command1 = ('@1,p2.@4,p1-270.')
                    command2 = ('@2,l70,l80,l90.')
                    command3 = ('@3,l70,l80,l90.')
                else:
                    command1 = ('@1,p2.@1,p2.@1,p2.@4,p1+270.')
                    command2 = ('@2,l71,l81,l91.')
                    command3 = ('@3,l71,l81,l91.')
        serial_write(command1)
        time.sleep(0.3)
        serial_write(command2)
        time.sleep(0.3)
        serial_write(command3)


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
            global fire_scenario
            global alarm_is_on
            if fire_scenario:
                if int(states[0]['value']) >= 610 and not alarm_is_on:
                    alarm_is_on = True
                    serial_write('@5,A31.')
                if int(states[0]['value']) < 610 and alarm_is_on:
                    alarm_is_on = False
                    serial_write('@5,A30.')
            app.log('gas', data.node_id, states)


if __name__ == '__main__':
    # MultiSensors
    app.add_thing('multisensor', '1')
    app.add_thing('multisensor', '2')
    app.add_thing('multisensor', '3')
    app.add_thing('multisensor', '4')
    app.add_thing('multisensor', '5')
    app.add_thing('gas', '9')

    # Lamps
    for i in range(1, 10):
        app.add_thing('lamp', '2:%d' % i)
        app.add_thing('lamp', '3:%d' % i)

    app.add_thing('cooler', '1:1')
    app.add_thing('valve', '4:2')
    app.add_thing('curtain', '4:1')
    app.add_thing('projector', '1:1')
    app.add_thing('tv', '1:1')
    app.add_thing('alarm', '5:3')
    app.add_thing('mode', 'presentation')
    app.add_thing('mode', 'fire')

    app.run()
    while True:
        try:
            serial_read()
        except Exception as e:
            logger.error(str(e))
