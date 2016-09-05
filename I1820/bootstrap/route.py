# In The Name Of God
# ========================================
# [] File Name : route.py
#
# [] Creation Date : 26-08-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
import flask
import json

from . import app


@app.route('/test')
def test_handler():
    return "18.20 is leaving us"


@app.route('/event/', methods=['POST'])
def thing_handler():
    data = flask.request.get_json(force=True)
    result = {}

    print(data)

    return json.dumps(result)
