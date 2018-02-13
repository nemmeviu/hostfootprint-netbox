#!/usr/bin/env python3

from netboxapi import NetboxAPI
import argparse
        
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
    help='Find and Print'
)
#
parser.add_argument(
    '--url',
    required=True,
     help='ex: http://netbox.domain.com/api/'
)

###
# process argparse
args = parser.parse_args()
#
parent = args.parent
search = args.search
boxurl = args.url
match = args.match
country = args.country
tenantgroup = args.tenantgroup
tenant = args.tenant
output = args.output

netbox = NetboxAPI()
netbox.conn(boxurl)
netbox.in_action(match=match, parent=parent, search=search)
netbox.output(output)
#netbox.parse_prefixes()

#test = NetboxAPI()
#test.parse_prefixes()
# print(test.get_nb_api('prefix'))

#netbox.parse_prefixes()
#print(json.dumps(netbox.get_nb_api('prefix', args.tenantgroup), indent=4, sort_keys=True))
#prefix = netbox.get_nb_api('prefix', 'all')
#print(json.dumps(prefix, indent=4, sort_keys=True))
#prefix = prefix['results']
#sites = netbox.get_nb_api('site', 'all')
#sites = sites['results']
##print(json.dumps(sites, indent=4, sort_keys=True))

#base_scan = netbox.base_scan(prefix, sites)
