#!/usr/bin/env python3

from I1820.I1820App import I1820App


if __name__ == '__main__':
    app = I1820App('192.168.1.9', 1373)
    app.start()
