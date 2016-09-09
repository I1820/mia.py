# In The Name Of God
# ========================================
# [] File Name : ping.py
#
# [] Creation Date : 09-09-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
import requests
import threading
import logging
from .. import i1820_id


log = logging.getLogger('ping')


class PingService:
    def __init__(self, i1820_base_url, things):
        self.base_url = i1820_base_url
        self.things = things

    def ping(self):
        message = {
            'rpi_id': str(i1820_id),
            'things': self.things
        }
        try:
            requests.post(self.base_url + 'discovery', json=message)
        except Exception as e:
            log.error('Ping request failed: %s' % e)
        threading.Timer(10, self.ping).start()
