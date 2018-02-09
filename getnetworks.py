#!/usr/bin/env python3

from netboxapi import NetboxAPI
import argparse
        
parser = argparse.ArgumentParser(
    description='Netbox API -> pynmap -> elasticsearch',
    epilog='hostfootprint with netbox, elasticsearch and nmap integration.'
)
parser.add_argument(
    '--country',
    dest='country',
    nargs='*',
    help='''Country: --country China'''
)
#
parser.add_argument(
    '--tenantgroup',
    dest='tenantgroup',
    nargs='*',
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
    nargs='*',
    required=True,
    help='''Get all Countries'''
)
#
parser.add_argument(
    '--print',
    dest='boxprint',
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
boxurl = args.url
boxprint = args.boxprint
country = args.country
tenantgroup = args.tenantgroup
tenant = args.tenant
output = args.output


netbox = NetboxAPI()
netbox.conn(boxurl)
netbox.in_action(boxprint=boxprint)
#netbox.in_action()

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
