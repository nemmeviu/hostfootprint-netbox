#!/usr/bin/env python3
#
# get networks prefix from Netbox API
# execute nmap on this networks
# save the result on elasticsearch DB
#
from netboxapi import NetboxAPI, ElsSaveMap

from multiprocessing import Manager
from multiprocessing.pool import ThreadPool
from threading import Thread, Lock

import argparse, sys, os, ipaddress, nmap, datetime
from datetime import time as timeee
import time

es_lock = Lock()

## ELASTICSEARCH index
d = datetime.date.today()
index = os.getenv('ES_INDEX', 'nmap')
index_type = os.getenv('ES_INDEX_TYPE', 'nmap')
index = index + '-' + d.strftime('%m%Y')


NMAPPROCS=int(os.getenv('NMAPPROCS', '20'))
HOSTSPROCS=int(os.getenv('HOSTSPROCS', '20'))
# windows = 'windows'
# linux = 'linux'

def syncronic():
    return shared_info['sync']

def get_hosts_and_clear():
    result = []
    while len(hosts_shared_lists) > 0:
        result.append(hosts_shared_lists.pop())
    #print('get host and clear')
    return(result)

def get_nets_and_clear():
    result = []
    while len(nets_shared_lists) > 0:
        result.append(nets_shared_lists.pop())
    return(result)

def print_host(host_args):
    es.es_save( *host_args )

def do_print():
    if syncronic():
        hosts_args = get_hosts_and_clear()
        for host_args in hosts_args:
            es.es_save( *host_args )
    else:
        pool = ThreadPool(processes=HOSTSPROCS)
        while not shared_info['finalizar'] or len(hosts_shared_lists) > 0:
            hosts_args = get_hosts_and_clear()
            if len(hosts_args) > 0:
                pool.map(print_host, hosts_args )
            time.sleep(1)

class CreateSubNetworks(object):
    def __init__(self):
        pass
    def make_subnetworks(self, network_object):
        print('loading network: %s' % network_object['prefix'])
        try:
            ip_net = ipaddress.ip_network(network_object['prefix'])
        except:
            ip_net = network_object['prefix']
        try:
            sub_net = ip_net.subnets(new_prefix=24)
            sub_net = list(sub_net)
        except:
            sub_net = [ ip_net ]
        return( [ ip_net ])

# nmap
def scan_net( subnet_object ):
    nm = nmap.PortScanner()
    nm.scan(
        hosts=subnet_object['net'],
        ports="445,22",
        arguments="-P0 -n --open"
    )

    for host in nm.all_hosts():
        # check if hosts exists:
        with es_lock:
            # ipaddress id on elasticsearch
            ipid = "%s-%s" % (host, es.check_time())
            body = {
                "query": {
                    "bool": {
                        "must":{ "term": { "_id": ipid } }
                    }
                }
            }
            exist = es.client.search(
                index=index,
                doc_type=index_type,
                body=body
            )
            
        try:
            old = exist['hits']['hits'][0]['_source']['ip']
        except:
            if nm[host].has_tcp(445) is True:
                hosts_shared_lists.append(
                    ('windows', host, subnet_object['netobject'])
                )
            if nm[host].has_tcp(22) is True:
                hosts_shared_lists.append(
                   ('linux', host, subnet_object['netobject'])
                )

def pipeline(n_list):

    shared_info['finalizar'] = False
    shared_info['sync'] = sync
    #shared_info['force'] = options['force']

    sub_net = CreateSubNetworks()
    for i in n_list:
        if 'prefix' in i.keys():
            list_sub_net = sub_net.make_subnetworks(i)
            for net in list_sub_net:
                nets_shared_lists.append(
                    {
                        'net': str(net),
                        'netobject': i
                    }
                )

    if syncronic():
        for net in nets_shared_lists:
            scan_net( net )
    else:
        t = Thread(target=do_print)
        t.start()

        pool = ThreadPool(processes=NMAPPROCS)
        while len(nets_shared_lists) > 0:
            nets = get_nets_and_clear()
            if len(nets) > 0:
                pool.map(scan_net, nets)
            time.sleep(1)
            #pool.close()
            #pool.join()

        shared_info['finalizar'] = True
        t.join()

#########
# argparse
parser = argparse.ArgumentParser(
    description='Netbox API -> pynmap -> elasticsearch',
    epilog='hostfootprint with netbox, elasticsearch and nmap integration.'
)
parser.add_argument(
    '--parent',
    dest='parent',
    required=True,
    help='Parent: --parent tenent'
)
#
parser.add_argument(
    '--search',
    dest='search',
    required=True,
    help='search: --search sites|tenacy|regions'
)
#
parser.add_argument(
    '--country',
    dest='country',
    help='Country: --country China'
)
#
parser.add_argument(
    '--tenantgroup',
    dest='tenantgroup',
    help='''Tenant group: --tenantgroup super-marketing'''
)
#
parser.add_argument(
    '--tenant',
    dest='tenant',
    nargs='*',
    help='''Tenant with spaces: --tenant jumbo'''
)
#
parser.add_argument(
    '--output',
    dest='output',
    required=True,
    help='''output: screen or db'''
)
#
parser.add_argument(
    '--match',
    dest='match',
    default=False,
    help='Find and Print'
)
#
parser.add_argument(
    '--role',
    dest='role',
    default=False,
    help='VLAN/Prefix Roles'
)
#
parser.add_argument(
    '--host',
    required=True,
    help='ex: netbox.domain.com'
)
#
parser.add_argument(
    '--port',
    default=80,
    type=int,
    help='ex: 80'
)

###
# process argparse
args = parser.parse_args()
#
parent = args.parent
search = args.search
match = args.match
country = args.country
tenantgroup = args.tenantgroup
tenant = args.tenant
output = args.output
host = args.host
port = args.port
role = args.role

###

manager = Manager()
hosts_shared_lists = manager.list([])
hosts_error_list = manager.list([])
nets_shared_lists = manager.list([])
shared_info = manager.dict()

###

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
    
es = ElsSaveMap(index, index_type)
netbox.search(**netbox_options)
n_list = netbox.output(output)
if output != 'screen':
    pipeline(n_list)
