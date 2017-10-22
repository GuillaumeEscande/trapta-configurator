#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re


from lib import adb

logger = logging.getLogger(__name__)

regex_mac_addr = re.compile(ur'((?:(\d{1,2}|[a-fA-F]{1,2}){2})(?::|-*)){6}')

def format(config, args, data_base):
    logger.info('Format of data %s', config.name)

    adbcon = adb.Adb(args.adb)
    logger.info('start adb server')
    adbcon.start_server()

    logger.info('Start format of device ')

    error = False

    logger.info('Activate wifi')
    # TODO

    logger.info('Find MAC Address')
    retcode, stdout, err = adbcon.shell("ip addr show wlan0", ["| grep 'link/ether '| cut -d' ' -f6"])

    if regex_mac_addr.match(stdout[:-1]) :
        mac_addr = stdout[:-1]
    else :
        logger.error("Wifi no enabled")
        error = True
    
    if not error :
        device = data_base.get( mac_addr )
        if device is None :
            logger.info('New device')

            logger.info('Find IMEI')
            retcode, stdout, err = adbcon.shell("service call iphonesubinfo 1", ["| awk -F \"'\" '{print $2}' | sed 's/[^0-9A-F]*//g' | tr -d '\n' && echo"])
            imei1 = stdout[:-1]

            device = dict()
            
            device['number'] = data_base.next_id()
            device['name'] = "TRAPTA-%03d" % (device['number'])
            device['mac'] = mac_addr 
            device['imei1'] = imei1
            device['licence'] = ""
            data_base.add( device )


    if not error : 
        logger.info('restore ap')
        adbcon.restore_img("backup.ap")

    if not error : 
        logger.info('Config of %s device', device['name'])

        logger.info('configure settings')
        for setting_namespace in config.settings:
            namespace = setting_namespace['namespace']
            for settings in setting_namespace['values']:
                adbcon.set_settings(namespace, settings['name'], settings['value'])
    
    if not error : 
        logger.info('remove packages')
        for package_name in config.app['removed']:
            adbcon.remove_app(package_name)

    if not error : 
        logger.info('hide packages')
        for package_name in config.app['hidded']:
            adbcon.hide_apk(package_name)

    if not error : 
        logger.info('install packages')
        for package_name in config.app['installed']:
            adbcon.install_apk(package_name)

    if not error :
        ## specific phone :
        adbcon.set_settings("global", "device_name", device['name'])

    if not error : 
        logger.info('Reboot device')
        adbcon.shell('reboot')



    logger.info('kill adb server')
    adbcon.kill_server()