#!/usr/bin/env python3
from subprocess import call, Popen

from I1820.app import I1820App
from I1820 import wapp

app = I1820App('192.168.128.90', 8080, '0.0.0.0', 1820)


@wapp.route('/open/<path:path>', methods=['GET'])
def open_slide_handler(path):
    Popen("xpdf -fullscreen ~/Desktop/%s " % path, shell=True)
    return ""


@wapp.route('/next', methods=['GET'])
def next_slide_handler():
    call(["./AoLab-Presenter/next.sh", "Page_Down"])
    return ""


@wapp.route('/back', methods=['GET'])
def back_slide_handler():
    call(["./AoLab-Presenter/next.sh", "Page_Up"])
    return ""


@wapp.route('/quit', methods=['GET'])
def quit_slide_handler():
    call(["./AoLab-Presenter/next.sh", "q"])
    return ""

if __name__ == '__main__':
    app.start()
    while True:
        pass
