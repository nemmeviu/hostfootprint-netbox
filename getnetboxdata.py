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
    '--parent','-p',
    dest='parent',
    required=True,
    help='Parent: --parent tenent'
)
#
parser.add_argument(
    '--search','-s',
    dest='search',
    required=True,
    help='search: --search sites|tenacy|regions'
)

###
# process argparse
args = parser.parse_args()


