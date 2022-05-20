#!/usr/bin/env python3

import os
from subprocess import Popen, call

import flask
from mia_py.I1820.app import I1820App
from werkzeug.utils import secure_filename

token = '83DB8F6299E0A303730B5F913B6A3DF420EBC2C2'

app = I1820App(token, '192.168.1.19')
wapp = flask.Flask("I1820-Presenter")


@wapp.route('/open/<path:path>', methods=['GET'])
def open_slide_handler(path):
    Popen("xpdf -fullscreen ./slides/%s " % path, shell=True)
    return ""


@wapp.route('/next', methods=['GET'])
def next_slide_handler():
    call(["./presenter.sh", "Page_Down"])
    return ""


@wapp.route('/back', methods=['GET'])
def back_slide_handler():
    call(["./presenter.sh", "Page_Up"])
    return ""


@wapp.route('/quit', methods=['GET'])
def quit_slide_handler():
    call(["./presenter.sh", "q"])
    return ""


@wapp.route('/upload', methods=['POST'])
def upload_slide_handler():
    # check if the post request has the file part
    if 'file' not in flask.request.files:
        return 'No file part'
    file = flask.request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('./slides', filename))
        return ''


if __name__ == '__main__':
    app.add_thing('service', '192.168.1.4:1820')
    app.run()
    wapp.run(host="0.0.0.0", port=1820, debug=False)
