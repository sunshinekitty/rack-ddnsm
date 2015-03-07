#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    rackddnsm.dnsapi
    ~~~~~

    Methods for utilizing Cloud DNS

    :copyright: (c) 2015 by Alex Edwards.
    :license: MIT, see LICENSE.txt for more details.

"""

import json
import requests
import sys

from rackddnsm.configuration import Settings
import rackddnsm.exceptions
from rackddnsm.http import APIcalls

class DNSService():
    
    def __init__(self, token, accountid, 
        endpoint="https://dns.api.rackspacecloud.com"):

        self.__endpoint = endpoint
        self.__accountid = accountid
        self.__DNS = APIcalls(token)

    """
        All of our GET methods
    """

    def get_domainid_by_name(self, domain):
        '''Returns domain ID based on domain name'''
        try:
            return (
                self.__DNS.get(
                    self.__endpoint + '/v1.0/' + self.__accountid + '/domains?name=' + domain
                )['domains'][0]['id']
            )
        except TypeError:
            raise rackddnsm.exceptions.RackddnsmNotFound('Domain not found')

    def get_records(self, domainid):
        '''Lists records for given domainid'''
        return (
            self.__DNS.get(
                self.__endpoint + '/v1.0/' + self.__accountid + '/domains/' + str(domainid) + '/records'
            )['records']
        )

    """
        All of our POST methods
    """

    def create_record(self, domain_id, data):
        '''Creates a new DNS record'''
        return (
            self.__DNS.post(
                self.__endpoint + '/v1.0/' + self.__accountid + '/domains/' + str(domain_id) + '/records', 
                data
            )
        )

    """
        All of our PUT methods
    """

    def update_record(self, domain_id, data):
        '''Updates a DNS record'''
        return (
            self.__DNS.put(
                self.__endpoint + '/v1.0/' + self.__accountid + '/domains/' + str(domain_id) + '/records',
                data
            )
        )
