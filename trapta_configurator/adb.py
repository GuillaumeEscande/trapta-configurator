#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
adb
a python interface for abd
"""

import logging
import subprocess

LOGGER = logging.getLogger(__name__)

ADB_PATH="adb"

class Adb(object):
  """A config for numeripi"""

  def __init__(self, path=ADB_PATH):
    """Initialize"""
    self.adb_path = path


  def __call(self, command, params=None ):
    cmd = [ADB_PATH, command]
    if params is not None:
      cmd.extend(params)
    LOGGER.debug('call_adb %s', " ".join(cmd))
    myPopen = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    stdout, stderr = myPopen.communicate()
    if myPopen.returncode != 0:
      LOGGER.error("calling : %s : %s", cmd, stderr)
    return myPopen.returncode, stdout, stderr
   
  def start_server(self):
    self.__call("start-server")
   
  def kill_server(self):
    self.__call("kill-server")
   
  def devices(self):
    retcode, out,err = self.__call("devices")
    list_device = []
    for line in out.split('\n')[1:]:
      if line :
        list_device.append(line.split())
    return list_device

  def shell(self, cmd):
    LOGGER.debug('shell %s', " ".join(cmd))
    return self.__call("shell", cmd)
   
  def set_settings(self, namespace, name, value):
    cmd = ["settings", "put", namespace, name, value]
    LOGGER.debug('set_settings %s', " ".join(cmd))
    retcode, out,err = self.shell(cmd)
      
  def remove_app(self, name):
    cmd = ["pm", "uninstall", "--user", "0", "-k", name]
    LOGGER.debug('remove_app %s', " ".join(cmd))
    retcode, out,err = self.shell(cmd)

  def install_apk(self, name):
    cmd = ["pm", "install", "./apk/"+name]
    LOGGER.debug('install_apk %s', " ".join(cmd))
    retcode, out,err = self.__call("install", cmd)

  def hide_apk(self, name):
    cmd = ["pm", "hide", name]
    LOGGER.debug('hide_apk %s', " ".join(cmd))
    retcode, out,err = self.__call("hide", cmd)
      
      
