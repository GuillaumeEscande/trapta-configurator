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
import sys
import json

import trapta_config
from commands import export
from commands import format
from lib import base

import _version

__version__ = _version.get_versions()['version']


ADB_PATH="adb"

LOGGER = logging.getLogger(__name__)
logging.root.setLevel( logging.INFO )

root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(logging.StreamHandler(sys.stdout))

def do_export(config, args, data_base):
    """Export repo"""
    export.export(config, args, data_base)

def do_format(config, args, data_base):
    """Format repo"""
    format.format(config, args, data_base)
    _ = data_base
    _ = args
    
def do_version(config, args, data_base):
    """Shows the version"""
    print(__version__)
    _ = args
    _ = data_base
    _ = config


def __add_command(subparsers, command, func):
    """Add the cnfig and verbose argument to given parser"""
    parser = subparsers.add_parser(command, help=command)
    if func is not None:
        parser.set_defaults(func=func)
    return parser


def main():
    """The main
    call trapta_configurator [--config CONFIG] update
    call trapta_configurator [--config CONFIG] export
    call trapta_configurator [--config CONFIG] import
    call trapta_configurator version
    """

    app_path = os.path.abspath(__file__)
    app_path = os.path.dirname(app_path)
    app_path = os.path.dirname(app_path)
    data_path = os.path.join(app_path, "data")

    config_path = os.path.join(data_path, "settings.json")
    base_path = os.path.join(data_path, "base.json")

    parser = argparse.ArgumentParser()
    parser.add_argument( '-c', '--config', default=config_path, help='The config file')
    parser.add_argument( '-b', '--base',  default=base_path, help='The base file')
    parser.add_argument( '-a', '--adb', default=None, help='The adb path')
    parser.add_argument( '-v', '--verbose', action='store_true', default=False, help='Go into verbose')

    subparser = parser.add_subparsers()

    # Commands update
    update_parser = __add_command(subparser, 'export', do_export)

    # Commands export
    export_parser = __add_command(subparser, 'format', do_format)

    # Commands version
    version_parser = __add_command(subparser, 'version', do_version)

    # args traitement
    args = parser.parse_args()
    config_file = args.config
    verbose = args.verbose

    if verbose:
        logging.root.setLevel(logging.DEBUG)
        LOGGER.setLevel(logging.DEBUG)
        LOGGER.info('%s with config %s', function.__name__, config_file)

    config = trapta_config.TraptaConfig.load(config_file)

    data_base = base.Base.load(args.base)

    args.func(config, args, data_base)

    data_base.dump(args.base)

if __name__ == '__main__':
    main()