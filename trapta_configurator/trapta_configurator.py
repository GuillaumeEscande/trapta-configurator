#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
trapta_configurator
a python service to configure Trapta android device
"""


import argparse
import logging
import os
import subprocess
import json

import adb

#from trapta_configurator import _version
#__version__ = _version.get_versions()['version']

ADB_PATH="adb"

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
logging.root.setLevel(logging.INFO)

logging.root.setLevel(logging.DEBUG)
LOGGER.setLevel(logging.DEBUG)

def main():
    adbcon = adb.Adb()
    LOGGER.info('start adb server')
    adbcon.start_server()

    LOGGER.info('list devices')
    print(adbcon.devices())

    with open("./conf/settings.json", 'r') as fson_fp:
        config = json.load(fson_fp)

    LOGGER.info('configure settings')
    for setting_namespace in config['settings']:
        namespace = setting_namespace['namespace']
        for settings in setting_namespace['values']:
            adbcon.set_settings(namespace, settings['name'], settings['value'])


    LOGGER.info('remove packages')
    for package_name in config['app']['removed']:
        adbcon.remove_app(package_name)

    LOGGER.info('hide packages')
    for package_name in config['app']['hidded']:
        adbcon.hide_apk(package_name)

    LOGGER.info('install packages')
    for package_name in config['app']['installed']:
        adbcon.install_apk(package_name)

    LOGGER.info('reboot device')
    adbcon.shell(['reboot'])


    LOGGER.info('kill adb server')
    adbcon.kill_server()



if __name__ == '__main__':
    main()