#!python
# -*- coding: UTF-8 -*-

import datetime
import time
import os

from pynetsh import NetshWLAN



def get_line(networks):
    return "{} - {}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), networks)


if __name__ == '__main__':

    netshwlan = NetshWLAN()

    while True:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "SSID.{}.log".format(datetime.datetime.now().strftime("%Y-%m-%d"))), "a") as ssid_log:
            line = get_line(netshwlan.get_networks(mode="bssid"))
            print(line)
            ssid_log.write(line)
            ssid_log.flush()
        time.sleep(1)
