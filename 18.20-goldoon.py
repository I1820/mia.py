#!/usr/bin/env python3
import flask

from I1820.app import I1820App
from I1820 import wapp

app = I1820App('127.0.0.1', 8080, '0.0.0.0', 3000)


@wapp.route('/goldoon', methods=['PUT'])
def goldon_handler():
    humidity = flask.request.form['humidity']
    app.log('temperature', '1', {'temperature': humidity})
    return ""


if __name__ == '__main__':
    app.add_thing('temperature', '0')
    app.start()
    while True:
        pass
