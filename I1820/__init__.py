import uuid
import requests
from flask import Flask

wapp = Flask("I1820-Plug")
i1820_id = uuid.uuid5(uuid.NAMESPACE_URL,
                      'I1820://%s.aolab.ceit.aut.ac.ir' % uuid.getnode())
i1820_session = requests.Session()
i1820_session.params.update(
    {'token': '83DB8F6299E0A303730B5F913B6A3DF420EBC2C2'})
