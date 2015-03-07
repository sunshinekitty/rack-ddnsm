#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    rackddnsm.configuration
    ~~~~~

    Utilities for configuring settings

    :copyright: (c) 2015 by Alex Edwards.
    :license: MIT, see LICENSE for more details.

"""

import json
import requests
import sys

from rackddnsm.http import rackspaceauth

class Settings():

    def __init__(self, username, apikey, auth_endpoint):
        self.__username        = username
        self.__apikey          = apikey
        self.__auth_endpoint   = auth_endpoint

    def auth(self):
        return(rackspaceauth(self.__username, self.__apikey, self.__auth_endpoint))
