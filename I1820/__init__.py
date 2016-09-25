import uuid
from flask import Flask

wapp = Flask("I1820-Plug")
i1820_id = uuid.uuid5(uuid.NAMESPACE_URL,
                      'I1820://%s.aolab.ceit.aut.ac.ir' % uuid.getnode())
