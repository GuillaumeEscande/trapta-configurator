#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

LOGGER = logging.getLogger(__name__)

def export(config, args, base):
    
    LOGGER.info('Export of data %s', config.name)
