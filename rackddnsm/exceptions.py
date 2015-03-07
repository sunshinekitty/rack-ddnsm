#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    rackddnsm.exceptions
    ~~~~~

    Exceptions for API calls

    :copyright: (c) 2015 by Alex Edwards.
    :license: MIT, see LICENSE for more details.

"""

class RackddnsmException(Exception):
    '''Rackddnsm fatal error'''
    
    def __init__(self, message):

        super(RackddnsmException, self).__init__(message)
        self.message = message

    def __string__(self):
        return repr(self.message)

class RackddnsmBadRequest(RackddnsmException):
    '''400 Bad Request'''
    pass

class RackddnsmUnauthorized(RackddnsmException):
    '''401 Unauthorized'''
    pass

class RackddnsmNotFound(RackddnsmException):
    '''404 Not Found'''
    pass

class RackddnsmServerError(RackddnsmException):
    '''Server Error 5xx'''
    pass
