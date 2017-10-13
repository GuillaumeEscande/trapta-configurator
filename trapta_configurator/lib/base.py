#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The base manager file
"""

import json

class Base( object ):
  """A config for tapta"""

  def __init__( self, json_data ):
    """Load"""
    self.json_data = json_data


  @staticmethod
  def load( json_path ):
    """Load a base contained in a JSON file"""
    with open( json_path, 'r' ) as fson_fp:
       return Base( json.load( fson_fp ) )


  def dump( self, path ):
    """Dump a base contained in a JSON file"""
    with open( path, 'w' ) as fson_fp:
      json.dump(self.json_data, fson_fp, sort_keys=True, indent=2)

  def get( self, mac ):
    for device in self.json_data['devices']:
      if device['mac'] == mac :
        return device  
    return None

  def add( self, device ):
    return self.json_data['devices'].append(device)

  def next_id( self ):
    if not self.json_data['devices']:
      return 1
    else :
      return self.json_data['devices'][-1]['number'] + 1