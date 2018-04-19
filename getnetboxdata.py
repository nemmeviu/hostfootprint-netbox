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
    help='Country: --country China'
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
#
parser.add_argument(
    '--esserver', '-e',
    dest='es_server',
    default='localhost',
    help='elasticsearch_server'
)
#
parser.add_argument(
    '--esport', '-ep',
    dest='es_port',
    type=int,
    default=9200,
    help='elasticsearch_port'
)

###
# process argparse
args = parser.parse_args()
#
match = args.match
parent = args.parent
search = args.search
country = args.country
tenantgroup = args.tenantgroup
tenant = args.tenant
output = args.output
host = args.host
port = args.port
role = args.role
es_server = args.es_server
es_port = args.es_port

##
netbox = NetboxAPI()
netbox.conn(host, port)

netbox_options = {
    'parent': parent,
    'search': search
}

if match:
    netbox_options['match_type'] = 'match'
    netbox_options['match'] = match
else:
    netbox_options['match_type'] = 'all'
    netbox_options['match'] = False

if role:
    netbox_options['role'] = role

try:
    sync = os.getenv('SYNC')
    if sync == 0:
        print('sync off!')
        sync = True
    else:
        sync = False
except:
    sync = False


#######


if match != 'all':
    netresult = netbox.search(match_type='match', match=match, parent=parent, search=search)
else:
    netresult = netbox.search(match_type='all', match=match, parent=parent, search=search)
print(netresult)
