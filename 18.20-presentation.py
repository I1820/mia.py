#!/usr/bin/env python3
from subprocess import call

from I1820.app import I1820App
from I1820 import wapp

app = I1820App('127.0.0.1', 8080, '0.0.0.0', 3000)


@wapp.route('/next', methods=['GET'])
def next_slide_handler():
    call(["for w in `xdotool search LibreOffice` ; do xdotool key --window $w Page_Down ; done"])
    return ""


if __name__ == '__main__':
    app.start()
    while True:
        pass
