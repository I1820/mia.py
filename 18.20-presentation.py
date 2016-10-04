#!/usr/bin/env python3
from subprocess import call

from I1820.app import I1820App
from I1820 import wapp

app = I1820App('192.168.128.90', 8080, '0.0.0.0', 1820)


@wapp.route('/next', methods=['GET'])
def next_slide_handler():
    call(["./next.sh"])
    return ""


if __name__ == '__main__':
    app.start()
    while True:
        pass
