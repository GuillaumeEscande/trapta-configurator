#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
adb
a python interface for abd
"""

import logging
import subprocess
import os

LOGGER = logging.getLogger(__name__)

if os.name == 'nt':
    ADB_PATH="adb.exe"
else:
    ADB_PATH="adb"

class Adb(object):
  """A config for numeripi"""

  def __init__(self, adb=None):
    """Initialize"""
    if adb is not None :
      LOGGER.warning("Utilisation adb path special %s", adb)
      self.adb_path = adb
    else :
      self.adb_path = ADB_PATH


  def __call(self, command=None, params=None, post=None ):
    cmd = [self.adb_path]

    cmd.append(command)

    if params is not None:
      cmd.append(params)

    if post is not None:
      cmd.extend(post)
    print(cmd)
    LOGGER.debug('call_adb %s', " ".join(cmd))
    myPopen = subprocess.Popen(" ".join(cmd), stdin = subprocess.PIPE, stdout = subprocess.PIPE, shell=True)
    stdout, stderr = myPopen.communicate()
    if myPopen.returncode != 0:
      LOGGER.error("calling : %s : %s", cmd, stderr)
    return myPopen.returncode, stdout, stderr
   
  def start_server(self):
    self.__call(command="start-server")
   
  def kill_server(self):
    self.__call(command="kill-server")
   
  def devices(self):
    retcode, out,err = self.__call(command="devices")
    list_device = []
    for line in out.split('\n')[1:]:
      if line :
        list_device.append(line.split())
    return list_device

  def shell(self, cmd="", post=None):
    LOGGER.debug('shell %s', cmd)
    return self.__call("shell", cmd, post)
   
  def set_settings(self, namespace="", name="", value=""):
    cmd = ["settings", "put", namespace, name, value]
    cmd_joined = " ".join(cmd)
    LOGGER.debug('set_settings %s', cmd_joined)
    retcode, out,err = self.shell(cmd_joined)
      
  def remove_app(self, name=""):
    LOGGER.debug('remove_app %s', name)
    retcode, out,err = self.__call("uninstall", name)

  def install_apk(self, name=""):
    package = "./data/apk/"+name
    LOGGER.debug('install_apk %s', package)
    retcode, out,err = self.__call("install", package)

  def hide_apk(self, name=""):
    cmd = ["pm", "hide", "--user", "0", "-k", name]
    cmd_joined = " ".join(cmd)
    LOGGER.debug('hide_apk %s', cmd_joined)
    retcode, out,err = self.shell(cmd_joined)
      
      
