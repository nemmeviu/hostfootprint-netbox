#!/usr/bin/env python3
#
# get network prefix from Netbox API
# execute nmap on this networks
# save the result on elasticsearch DB
#
from netboxapi import NetboxAPI

from multiprocessing import Manager
from multiprocessing.pool import ThreadPool
from threading import Thread, Lock

import argparse, sys, os, ipaddress, nmap, datetime, json, time
from datetime import time as timee

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
        # gracias fregular old: return(ip_net)
        return(sub_net)

##########
# argparse
parser = argparse.ArgumentParser(
    description='''
    Map networks based on Netbox IPAM Project.
    Generate one dashboard with netbox register information.
    Use elasticsearch in all modes''',
    epilog='Making inventory about your network!'
)

################################################################################
#  required argparses                                                          #
################################################################################
parser.add_argument(
    '--host', '-H',
    dest='host',
    required=True,
    help='The netbox url. Ex: netbox.domain.com'
)
#
parser.add_argument(
    '--port', '-p',
    dest='port',
    required=True,    
    default=80,
    type=int,
    help='ex: 80'
)
#
parser.add_argument(
    '--type', '-t',
    dest='search_type',
    required=True,
    help='values: dashboard|prefix'
)
#
parser.add_argument(
    '--output', '-o',
    dest='output',
    required=True,
    help='''output: screen or db'''
)

################################################################################
#  optional argparses                                                          #
################################################################################
# optional argparses: if type prefix                                           #
#
parser.add_argument(
    '--role', '-r',
    dest='role',
    default=False,
    help='VLAN/Prefix Roles'
)
#
parser.add_argument(
    '--parent', '-P',
    dest='parent',
    default='tenant',
    help='values: tenent'
)
#
parser.add_argument(
    '--search', '-s',
    dest='search',
    default='tenant',
    help='search: --search site|tenant'
)
#
parser.add_argument(
    '--country', '-C',
    dest='country',
    help='Country: --country China'
)
#
parser.add_argument(
    '--tenant', '-T',
    dest='tenant',
    nargs='*',
    help='tenant with spaces: --tenant jumbo'
)
#
parser.add_argument(
    '--tenantgroup', '-tg',
    dest='tenantgroup',
    help= 'tenant group: --tenantgroup super-marketing'
)
#
parser.add_argument(
    '--match', '-m',
    dest='match',
    default=False,
    help='Find and Print'
)
################################################################################
# optional argparses: if output db                                             #
parser.add_argument(
    '--esserver', '-es',
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
#
###

######## process argparse
args = parser.parse_args()
## required
host = args.host
port = args.port
search_type = args.search_type
output = args.output

## optional
role = args.role
parent = args.parent
search = args.search
country = args.country
tenant = args.tenant
ntenantgroup = args.tenantgroup
match = args.match

## elasticsearch
es_server = args.es_server
es_port = args.es_port

if search_type == 'dashboard':
    index = 'netbox-dashboard'
    index_type = 'netbox'
    save_es = 'save_dashboard'
else:
    save_es = 'es_save'
    ##
netbox = NetboxAPI()
netbox.conn(host, port)

netbox_options = {
    'search_type': search_type, 
    'parent': parent, 
    'search': search 
}

if match == False:
    netbox_options['match_type'] = 'all'
    netbox_options['match'] = match
else:
    netbox_options['match_type'] = 'match'
    netbox_options['match'] = match

if role:
    netbox_options['role'] = role

sync = False    
try:
    sync = os.getenv('SYNC')
    if sync == 0:
        print('sync off!')
        sync = True
except:
    pass


#######
netbox.search(**netbox_options)
n = netbox.output()

####################
# db output
if output == 'db':
    from netboxapi import ElsSaveMap
    es = ElsSaveMap(index, index_type)
    getattr(es, save_es)(n)
    
    ### if !sites and db here ... sys.exit(0)
    #if netbox_options['search'] != 'site':
    #print('''\nWarning ...
    #Only search:site can be sended to elasticsearch, try output screen.''')
    #sys.exit(0)
if output == 'screen':
    print(json.dumps(n, indent=4, sort_keys=True))        
   #pipeline(n_list)

#n_list = netbox.output(output)
#if output != 'screen':
#

#print(netresult)
