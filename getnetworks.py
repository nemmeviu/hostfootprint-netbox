#!/usr/bin/env python3
# 
# get networks prefix from Netbox API
# execute nmap on this networks
# save the result on elasticsearch DB
#
from netboxapi import NetboxAPI

from elasticsearch import Elasticsearch

from multiprocessing import Manager
from multiprocessing.pool import ThreadPool
from threading import Thread, Lock

import argparse, sys, time, os, ipaddress, nmap, datetime

d = datetime.date.today()
index= 'nmap-' + d.strftime('%m%Y')
es_lock = Lock()

#es = ElsSaveMap(index, index)

## ELASTICSEARCH index
#NMAPPROCS=int(os.getenv('NMAPPROCS'))
#HOSTSPROCS=int(os.getenv('HOSTSPROCS'))
## windows = 'windows'
## linux = 'linux'

def syncronic():
    return shared_info['sync']

def get_hosts_and_clear():
    result = []
    while len(hosts_shared_lists) > 0:
        result.append(hosts_shared_lists.pop())
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

class ElsSaveMap(object):                                                                                                                                                                                                       
    def __init__(self, object_type, doc_type):
        '''
        init global variables
        pass host to elasticsearch connect
        '''
        self.client = Elasticsearch(
            hosts=[ settings.ELASTICSEARCH ]
        )

        self.object_type = object_type
        self.doc_type = doc_type

    def check_time(self):
        ''' sub_net = ip_net.subnets(new_prefix=24)
        import datetimeist(sub_net)
        20:00 - 06:00 = ip-20-06
        06:00 - 20:00 = ip-06-20
        return( [ ip_net ]) 
        return('xx-xx')
        '''
        
        datenow = datetime.now()
        timenow = datenow.time()

        start = time(6, 0, 0)
        end = time(20, 0, 0)

        timestr = datenow.strftime("%y%m%d")

        if timenow >= start and timenow < end:
            return(timestr + '-06-20')
        else:
            return(timestr + '-20-06')

    def es_save(self, map_type, host, n_object):

        #"g_businessunit": 
        #"g_flag": "goncalves-house",
        #"local_address": "Pasaje Los Guindos 9227 - La Florida",
        #"location": "goncalves-house",
        #"prefix": "192.168.1.0/24",
        #"status": 0

        attribute = {
            'map_type': map_type,
            'ip': host,
            'network': networklist['prefix'],
            'country': networklist['prefix'],
            'city': networklist['prefix'],
            'businessunit': networklist['prefix'],
            'flag': networklist['prefix'],
            'local_id': networklist['prefix'],
            'local_address': networklist['prefix'],
            'local_desc': networklist['prefix'],
            'geo_point': {
                'lat': netobject.local.lat,'_source']['ip']
                'lon': netobject.local.lon
            }
        }

        normalize = ''.join(c.lower() for c in host if not c.isspace())
        today = datetime.today().strftime("%m%d%Y")

        data = datetime.now()
        date_els = int( data.timestamp() * 1000 )

        attribute['created_at'] = date_els
    
        # old 1['finalizar'] = False
        #_id=(normalize + '-' + today)
        # old 2o['force'] = options['force']
        #_id=(normalize + '-' + str(date_els))

        _id=(normalize + '-' + self.check_time())

        response = self.client.index(
            index=self.object_type,
            id=_id,
            doc_type=self.doc_type,
            body=attribute
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
        db.connections.close_all()
    
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

    
sync = True    
netbox.search(**netbox_options)
networlist = netbox.output(output)
pipeline(networlist)
