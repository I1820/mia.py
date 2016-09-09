#!/usr/bin/env python3

from I1820.app import I1820App

app = I1820App('192.168.1.9', 1373)


@app.notification('lamp')
def lamp_notification(data: dict):
    print(data)

if __name__ == '__main__':
    app.start()
