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
            networks = netshwlan.get_networks(mode="bssid", signal_limit=50)
            profiles = netshwlan.get_profiles()
            network_set = set([n.name for n in networks])
            profile_set = set([p.name for p in profiles])
            intersect = network_set & profile_set
            known_networks = []
            for network in networks:
                if network.name in intersect:
                    networks.remove(network)
                    known_networks.append(network)
            line = get_line(known_networks + networks)
            print(line)
            ssid_log.write(line)
            ssid_log.flush()
        time.sleep(1)
