# In The Name Of God
# ========================================
# [] File Name : route.py
#
# [] Creation Date : 09-09-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
import flask
import json
from ..app import I1820App

from . import app


@app.route('/event', methods=['POST'])
def notification_handler():
    data = flask.request.get_json(force=True)
    result = I1820App.notification_handler(data)
    return json.dumps(result)
