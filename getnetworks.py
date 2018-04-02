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

import argparse, sys, os, ipaddress, nmap, datetime
from datetime import time as timeee
import time


d = datetime.date.today()
index = os.getenv('ES_INDEX', 'nmap')
index_type = os.getenv('ES_INDEX_TYPE', 'nmap')
index = index + '-' + d.strftime('%m%Y')
es_lock = Lock()

mapping = {
    "settings" : {
        "analysis": {
            "normalizer": {
                "my_normalizer": {
                    "type": "custom",
                    "char_filter": [],
                    "filter": ["lowercase", "asciifolding"]
                }
            }
        },
        "max_result_window": 35000,
        "number_of_shards" : 5,
        "number_of_replicas" : 1,
    },
    "mappings": {
        index_type:{
            "properties": {
                "g_last_mod_date": {
	            "type": "date",
	            "format": "epoch_millis"
                },
                "g_country": {
                    "index": "true", 
                    "type": "keyword",
                    "normalizer": "my_normalizer"
                },
                "g_flag": {
                    "index": "true", 
                    "type": "keyword",
                    "normalizer": "my_normalizer"                    
                },
                "g_businessunit": {
                    "index": "true", 
                    "type": "keyword",
                    "normalizer": "my_normalizer"
                },
                "g_application": {
                    "index": "true", 
                    "type": "keyword",
                    "normalizer": "my_normalizer"
                },
                "g_kpi": {
	            "type": "boolean"
                },
                "g_critical": {
	            "type": "boolean"
                },
                "situation": {
                    "index": "true", 
                    "type": "keyword"
                },
                "physical_address": {
                    "index": "true", 
                    "type": "keyword",
                    "normalizer": "my_normalizer"
                },
                "city": {
                    "index": "true", 
                    "type": "keyword",
                    "normalizer": "my_normalizer"
                },
                "geo_location": {
	            "type": "geo_point"
                },
	        "local_desc": {
	            "index": "true", 
                    "type": "keyword",
                    "normalizer": "my_normalizer"
                },
                "map_type": {
                    "index": "true", 
                    "type": "keyword"
                },
                "local_id": {
                    "index": "true", 
                    "type": "keyword",
                    "normalizer": "my_normalizer"
                },
	        "local_address": {
	            "index": "true", 
                    "type": "keyword",
                    "normalizer": "my_normalizer"
                },
                "sites": {
	            "type": "integer"
                },
                "network": {
                    "index": "true", 
                    "type": "keyword"
                },
                "role": {
                    "index": "true", 
                    "type": "keyword"
                },
                "ip": {
                    "type": "ip"
                },
	        "hostname": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "parsed": {
                    "type": "short"
	        },
	        "exit_code": {
                    "type": "short"
	        },
	        "Caption": {
	            "index": "true", 
                    "type": "keyword"
	        },	    
	        "FreePhysicalMemory": {
	            "type": "long"
	        },
	        "TotalPhysicalMemory": {
	            "type": "long"
	        },
	        "Model": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "CurrentTimeZone": {
	            "type": "short"
	        },
	        "DaylightInEffect": {
	            "type": "boolean"
	        },
	        "EnableDaylightSavingsTime": {
	            "type": "boolean"
	        },
	        "NumberOfLogicalProcessors": {
	            "type": "short"
	        },
	        "NumberOfProcessors": {
	            "type": "short"
	        },
	        "ProcFamily": {
	            "type": "short"
	        },
	        "ProcLoadPercentage": {
	            "type": "short"
	        },
	        "ThermalState": {
	            "type": "short"
	        },
	        "Vendor": {
	            "index": "true",
                    "type": "keyword"
	        },
	        "err": {
	            "index": "true",
                    "type": "keyword"
	        },
	        "ProcManufacturer": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "ProcName": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "Status": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "SystemType": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "IdentifyingNumber": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "LoadPercentage": {
	            "type": "short"
	        },
	        "Manufacturer": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "Name": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "CSName": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "LastBootUpTime": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "ServicePackMajorVersion": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "HotFixID": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "OSArchitecture": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "Product": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "SerialNumber": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "UUID": {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "UserName": {
	            "index": "true", 
                    "type": "keyword",
                    "normalizer": "my_normalizer"
	        },
	        "Version" : {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "Name_AV" : {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "Version_AV" : {
	            "index": "true", 
                    "type": "keyword"
	        },
	        "HotFixID" : {
	            "index": "true", 
                    "type": "keyword"
	        },
                "DHCPServer": {
                    "index": "true", 
                    "type": "keyword"
	        },
                "IPAddress": {
                    "index": "true", 
                    "type": "keyword"
	        },
                "MACAddress": {
                    "index": "true", 
                    "type": "keyword"
	        },
                "ServiceName": {
                    "index": "true", 
                    "type": "keyword"
	        }
            }
        }
    }
}

## ELASTICSEARCH index
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

class ElsSaveMap(object):
    def __init__(self, index, index_type): 
        '''
        init global variables
        pass host to elasticsearch connect
        '''
        self.client = Elasticsearch(
            hosts=[ os.getenv('ES_SERVER', '127.0.0.1') ]
        )

        self.index = index
        self.doc_type = index_type

        try:
            self.client.search(index=self.index)
        except:
            print('creating... %s' % self.index)
            new_index = self.client.indices.create(index=self.index, ignore=400, body=mapping)
            print(new_index)

    def check_time(self):
        ''' sub_net = ip_net.subnets(new_prefix=24)
        import datetimeist(sub_net)
        20:00 - 06:00 = ip-20-06
        06:00 - 20:00 = ip-06-20
        return( [ ip_net ])
        return('xx-xx')
        '''

        datenow = datetime.datetime.now()
        timenow = datenow.time()

        start = timeee(6, 0, 0)
        end = timeee(20, 0, 0)

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

        attribute = {}

        attribute['g_kpi'] = False
        attribute['g_critical'] = False
        try:
            attribute['map_type'] = map_type
        except:
            pass
        try:
            attribute['ip'] = host
        except:
            pass
        try:
            attribute['role'] = n_object['role']
        except:
            pass
        try:
            attribute['network'] = n_object['prefix']
        except:
            pass
        try:
            attribute['g_country'] = n_object['g_country']
        except:
            pass
        try:
            attribute['g_flag'] = n_object['g_flag']
        except:
            pass
        try:            
            attribute['g_businessunit'] = n_object['g_businessunit']
        except:
            pass
        try:
            attribute['local_id'] = n_object['local_id']
        except:
            pass
        try:
            attribute['physical_address'] = n_object['physical_address']
        except:
            pass
        try:
            attribute['local_desc'] = n_object['comments']
        except:
            pass
        
        try:
            attribute['geo_location'] = {
                'lat': n_object['custom_fields']['latitud'],
                'lon': n_object['custom_fields']['latitud']
            }
        except:
            pass

        normalize = ''.join(c.lower() for c in host if not c.isspace())
        today = datetime.date.today().strftime("%m%d%Y")

        data = datetime.datetime.now()
        date_els = int( data.timestamp() * 1000 )

        attribute['g_last_mod_date'] = date_els

        # old 1['finalizar'] = False
        #_id=(normalize + '-' + today)
        # old 2o['force'] = options['force']
        #_id=(normalize + '-' + str(date_els))

        _id=(normalize + '-' + self.check_time())

        try:
            response = self.client.index(
                index=self.index,
                id=_id,
                doc_type=self.doc_type,
                body=attribute
            )
        except:
            print('fail in _id: %s' % _id )

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
