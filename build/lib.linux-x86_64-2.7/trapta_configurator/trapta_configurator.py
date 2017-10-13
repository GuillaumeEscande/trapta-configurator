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

import trapta_config
from commands import export
from commands import format


__version__ = _version.get_versions()['version']


ADB_PATH="adb"

LOGGER = logging.getLogger(__name__)
logging.root.setLevel( logging.INFO )


def do_export(config, args):
    """Export repo"""
    export.export(config)
    _ = args

def do_format(config, args):
    """Format repo"""
    format.format(config)
    _ = args
    
def do_version(config, args):
    """Shows the version"""
    print(__version__)
    _ = args


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

    parser = argparse.ArgumentParser()
    parser.add_argument( '-c', '--config', help='The config file')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Go into verbose')

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

    config = trapta_config.PupyConfig.load(config_file)

    args.func(config, args)

if __name__ == '__main__':
    main()