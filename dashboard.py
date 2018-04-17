#!/usr/bin/env python3
from netboxapi import NetboxAPI, ElsSaveMap
import argparse

parser = argparse.ArgumentParser(
    description='Netbox API -> pynmap -> elasticsearch',
    epilog='View sites without load information. Send the resume to elasticserch'
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
    default='site',
    help='search: --search sites|tenacy|regions. Default is "sites"'
)
#
parser.add_argument(
    '--tenantgroup',
    dest='tenantgroup',
    help='Tenant group: --tenantgroup super-marketing'
)
#
parser.add_argument(
    '--tenant',
    dest='tenant',
    nargs='*',
    help='Tenant with spaces: --tenant jumbo'
)
#
parser.add_argument(
    '--output',
    dest='output',
    required=True,
    help='output: screen or db'
)
#
parser.add_argument(
    '--match',
    dest='match',
    default='all',
    help='Find and Print'
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
#
parser.add_argument(
    '--esserver',
    dest='es_server',
    default='localhost',
    help='elasticsearch_server'
)
#
parser.add_argument(
    '--esport',
    dest='es_port',
    type=int,    
    default=9200,
    help='elasticsearch_port'
)

###
# process argparse
args = parser.parse_args()
#
parent = args.parent
search = args.search
match = args.match
tenantgroup = args.tenantgroup
tenant = args.tenant
output = args.output
host = args.host
port = args.port
es_server = args.es_server
es_port = args.es_port

netbox = NetboxAPI()
netbox.conn(host, port)
if match != 'all':
    netresult = netbox.search(match_type='match', match=match, parent=parent, search=search)
else:
    netresult = netbox.search(match_type='all', match=match, parent=parent, search=search)
print(netresult)    

#es = ElsSaveMap(index, index_type)    
#es.save_dashboard(output, es_server, es_port)
