#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    rackddnsm.http
    ~~~~~

    Classes for all API calls

    :copyright: (c) 2015 by Alex Edwards.
    :license: MIT, see LICENSE for more details.

"""

import json
import requests
import sys

import rackddnsm.exceptions

def handle_error(req):
    '''Handle our errors'''
    code = req.status_code
    # First key is error message always, look in that dict for msg
    message = req.json()['message']

    error_map = {
        400: rackddnsm.exceptions.RackddnsmBadRequest(message),
        401: rackddnsm.exceptions.RackddnsmUnauthorized(message),
        404: rackddnsm.exceptions.RackddnsmNotFound(message),
        500: rackddnsm.exceptions.RackddnsmServerError(message),
        501: rackddnsm.exceptions.RackddnsmServerError(message),
        502: rackddnsm.exceptions.RackddnsmServerError(message),
        503: rackddnsm.exceptions.RackddnsmServerError(message),
        504: rackddnsm.exceptions.RackddnsmServerError(message),
        505: rackddnsm.exceptions.RackddnsmServerError(message),
    }
    if code in error_map:
        raise error_map[code]
    if code not in range(200, 300):
        raise rackddnsm.exceptions.RackddnsmException(message)

def rackspaceauth(raxusername, raxapikey, endpoint):
    # Tell it what we're sending/receiving
    token_headers = { 'Accept': 'application/json',
                      'Content-Type': 'application/json'}
        
    # POST our login creds
    token_login = { 'auth': {
        'RAX-KSKEY:apiKeyCredentials': {
          'username': raxusername,
            'apiKey': raxapikey
        },
    }}

    # Send POST to identity endpoint
    req = requests.post(
        endpoint,
        data=json.dumps(token_login),
        headers=token_headers, 
        verify=False
    )

    if req.status_code in range(200, 300):
        response = json.loads(req.text)
        token = response["access"]["token"]["id"]
        uid   = response["access"]["user"]["id"]
        uid   = response["access"]["token"]["tenant"]["id"]
        return [token,uid]
    else:
        handle_error(req)

class APIcalls():
    
    def __init__(self, token):
        self.__token    = token

    def __headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Auth-Token': self.__token,
        }

    def get(self, url):
        '''Make a HTTP/HTTPS GET request'''
        req = requests.get(url, headers=self.__headers(), verify=False)
        if req.status_code in range(200, 300):
            return json.loads(req.text)
        else:
            handle_error(req)

    def post(self, url, data):
        '''Make a HTTP/HTTPS POST request'''
        req = requests.post(url, headers=self.__headers(), 
            data=json.dumps(data), verify=False)
        if req.status_code in range(200, 300):
            return json.loads(req.text)
        else:
            handle_error(req)

    def put(self, url, data):
        '''Make a HTTP/HTTPS PUT request'''
        req = requests.put(url, headers=self.__headers(), 
            data=json.dumps(data), verify=False)
        if req.status_code in range(200, 300):
            return json.loads(req.text)
        else:
            handle_error(req)

    def delete(self, url):
        '''Make a HTTP/HTTPS DELETE request'''
        req = requests.delete(url, headers=self.__headers(), verify=False)
        if req.status_code in range(200, 300):
            return True
        else:
            handle_error(req)
