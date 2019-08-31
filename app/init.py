#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import threading


def serverdb():
    os.system('python3 -u /home/app/server.py')
    return


def serverapi():
    os.system('python3 -u /home/app/frontserver.py')
    return


if __name__ == "__main__":
    t = threading.Thread(target=serverdb)
    t.start()
    t = threading.Thread(target=serverapi)
    t.start()
