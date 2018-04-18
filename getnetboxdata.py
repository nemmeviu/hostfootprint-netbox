#!/usr/bin/env python3
#
# get network prefix from Netbox API
# execute nmap on this networks
# save the result on elasticsearch DB
#
from netboxapi import NetboxAPI, ElsSaveMap

from multiprocessing import Manager
from multiprocessing.pool import ThreadPool
from threading import Thread, Lock

import argparse, sys, os, ipaddress, nmap, datetime
from datetime import time as timee
import time

es_lock = Lock()

## ELASTICSEARCH index
d = datetime.date.today()
index = os.getenv('ES_INDEX', 'nmap')
index_type = os.getenv('ES_INDEX_TYPE', 'nmap')
index = index + '-' +d.strftime('%m%Y')

NMAPPROCS=int(os.getenv('NMAPPROCS', '20'))
HOSTSPROCS=int(os.getenv('HOSTSPROCS', '20'))


class CreateSubNetworks(object):
    '''
    The class CreateSubNetworks receives a object (network) and
    split the network in many prefixes /24.
    '''

    def __init__(self):
        pass
    def make_subnetworks(self, network_prefix):
        print('loading network: %s' % network_prefix)
        try:
            ip_net = ipaddress.ip_network(network_prefix)
        except:
            ip_net = network_prefix
        try:
            sub_net = ip_net.subnets(new_prefix=24)
            sub_net = list(sub_net)
        except:
            sub_net = [ ip_net ]
        return(sub_net)

##########
# argparse
parser = argparse.ArgumentParser(
    description='Netbox API -> pynmap -> elasticsearch',
    epilog='hostfootprint with netbox, elasticsearch and nmap integration.'
)
parser.add_argument(
    '--parent', '-P',
    dest='parent',
    required=True,
    help='Parent: --parent tenent'
)
#
parser.add_argument(
    '--search', '-s',
    dest='search',
    required=True,
    help='search: --search sites|tenacy|regions'
)
#
parser.add_argument(
    '--country', '-c',
    dest='country',
    required=True,
    help='search: --search sites|tenacy|regions'
)
#
parser.add_argument(
    '--tenantgroup', '-tg',
    dest='tenantgroup',
    help= '''Tenant group: --tenantgroup super-marketing'''
)
#
parser.add_argument(
    '--tenant', '-t',
    dest='tenant',
    nargs='*',
    help='''Tenant with spaces: --tenant jumbo'''
)
#
parser.add_argument(
    '--output', '-o',
    dest='output',
    required=True,
    help='''output: screen or db'''
)
#
parser.add_argument(
    '--match', '-m',
    dest='match',
    default=False,
    help='Find and Print'
)
#
parser.add_argument(
    '--role', '-r',
    dest='role',
    default=False,
    help='VLAN/Prefix Roles'
)
#
parser.add_argument(
    '--host', '-H',
    required=True,
    help='ex: netbox.domain.com'
)
#
parser.add_argument(
    '--port', '-p',
    default=80,
    type=int,
    help='ex: 80'
)

###
# process argparse
args = parser.parse_args()
parent = args.parent
search = args.match
country = args.country
tenantgroup = args.tenantgroup
tenant = args.tenant
output = args.output
host = args.host
port = args.port
role = args.role
