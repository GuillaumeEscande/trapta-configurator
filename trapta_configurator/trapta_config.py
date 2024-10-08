#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The trapta configuration module
"""

import json

class TraptaConfig( object ):
    """A config for tapta"""

    def __init__( self, json_data ):
        """Initialize"""
        self.json_data = json_data

    @staticmethod
    def load( json_path ):
        """Load a tapta contained in a JSON file"""
        with open( json_path, 'r' ) as fson_fp:
            return TraptaConfig( json.load( fson_fp ) )

    @property
    def name( self ):
        """
        Return name string
        """
        return self.json_data["name"] 

    @property
    def settings( self ):
        """
        Return settings string
        """
        return self.json_data["settings"] 

    @property
    def app( self ):
        """
        Return app string
        """
        return self.json_data["app"] 