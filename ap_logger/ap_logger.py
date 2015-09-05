#!python3
# -*- coding: UTF-8 -*-

import datetime
import logging
import time
import os

from pynetsh import NetshWLAN



def get_line(networks):
    return "{} - {}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), networks)


if __name__ == '__main__':

    AP_LOGGER_PATH = os.path.dirname(os.path.abspath(__file__))
    
    SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
    DEFAULT_LOG_FILE = os.path.join(AP_LOGGER_PATH, "logs", "{}-{}.log".format(SCRIPT_NAME, datetime.datetime.now().strftime("%Y%m%d%H%M%S")))
    
    log_formatter = logging.Formatter("%(asctime)s -- %(levelname)s : %(name)s -- %(message)s")
    
    try:
        file_handler = logging.FileHandler(DEFAULT_LOG_FILE)
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(logging.DEBUG)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(DEFAULT_LOG_FILE))
    
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.DEBUG)
    
    logging.basicConfig(level=logging.DEBUG, format=log_formatter, handlers=[file_handler, console_handler])
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    try:
        netshwlan = NetshWLAN()

        while True:
            with open(os.path.join(AP_LOGGER_PATH, "logs", "SSID.{}.log".format(datetime.datetime.now().strftime("%Y-%m-%d"))), "a") as ssid_log:
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
                ssid_log.write(line)
                ssid_log.flush()
            time.sleep(60)
    except Exception as general_exception:
        logger.critical(general_exception)
