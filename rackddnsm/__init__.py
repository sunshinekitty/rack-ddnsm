#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    rackddnsm
    ~~~~~

    Dynamic DNS metadata for Rackspace Cloud DNS, 
    Manages TXT records containing metadata in the format of title,desc,data.

    :copyright: (c) 2015 by Alex Edwards.
    :license: MIT, see LICENSE for more details.

"""
import re

from rackddnsm.configuration import Settings
from rackddnsm.dnsapi import DNSService

class Rackddnsm():
    def __init__(self, username, apikey,
        auth_endpoint   = "https://identity.api.rackspacecloud.com/v2.0/tokens"):

        self.__settings = Settings(
            username        = username,
            apikey          = apikey,
            auth_endpoint   = auth_endpoint
        )

        auth_information = self.__settings.auth()
        
        self.__dns = DNSService(
            token      = auth_information[0],
            accountid  = auth_information[1]
        )

    def __get_domain_id(self, domain):
        '''Get domain ID given domain name'''
        return self.__dns.get_domainid_by_name(domain)

    def __get_record_id(self, domain, record_title):
        '''Get record ID based on metadata title'''
        domain_id = self.__dns.get_domainid_by_name(domain)
        records = self.__dns.get_records(domain_id)

        for record in records:
            if ( ( record['type'] == 'TXT' ) and ( bool(re.search('^rackddnsm:', record['data'])) ) ):
                ddnsm_title  = record['data'][10:].split(',|,')[0]
                if ( ddnsm_title == record_title ):
                    return record['id']

        return False
                

    def get_record_api(self, domain, title):
        '''Get rackddnsm TXT records'''
        domain_id = self.__dns.get_domainid_by_name(domain)
        records = self.__dns.get_records(domain_id)

        for record in records:
            if ( ( record['type'] == 'TXT' ) and ( bool(re.search('^rackddnsm:', record['data'])) ) ):
                ddnsm_data  = record['data'][10:].split(',|,')
                ddnsm_title = ddnsm_data[0]
                ddnsm_desc  = ddnsm_data[1]
                ddnsm_d     = ddnsm_data[2]
                if ( ddnsm_title == title ):
                    return {
                        'title': ddnsm_title,
                        'desc': ddnsm_desc,
                        'data': ddnsm_d
                    }

        return False

    def get_record_dns(self, domain, title, nameserver=False):
        '''Queries DNS to get rackddnsm TXT records'''
        # Not yet finished
        import dns.resolver
        resolver = dns.resolver.Resolver()

        if ( nameserver ):
            resolver.nameservers = [nameserver]

        print(resolver.query(domain, 'TXT'))

    def set_metadata(self, domain, title, desc, data):
        '''Sets metadata for given domain and title'''
        sep = ',|,'
        record_data = 'rackddnsm:' + title + sep + desc + sep + data
        record_id = self.__get_record_id(domain, title)
        domain_id = self.__get_domain_id(domain)

        if ( record_id ):
            # Update existing record
            update_data = {
                'records' : [ {
                    'id': record_id,
                    'name': domain,
                    'data': record_data,
                    'ttl': '300'
                } ]
            }
            self.__dns.update_record(domain_id, update_data)
        else:
            # Create a new record
            update_data = {
                'records' : [ {
                    'type': 'TXT',
                    'name': domain,
                    'data': record_data,
                    'ttl': '300'
                } ]
            }
            self.__dns.create_record(domain_id, update_data)
