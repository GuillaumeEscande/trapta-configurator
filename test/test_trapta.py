#!/usr/bin/env python
# -*- Coding:utf-8 -*-

import unittest
import sys
import logging

from trapta_configurator import trapta_configurator


class TestTrapta(unittest.TestCase):
    def test_command_update(self):
        sys.stdout = sys.__stdout__
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        root.addHandler(logging.StreamHandler(sys.stdout))
        sys.argv = ["trapta_configurator.py", "-c", "conf/test_conf.json", "update"]
        trapta_configurator.main()

if __name__ == "__main__":
    unittest.main()
