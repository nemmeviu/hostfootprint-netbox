#encoding=utf8

import sys
#from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from networks.models import *
from django.db.utils import IntegrityError

from django import db

import sys, time,os
from multiprocessing import Manager
#from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from threading import Thread, Lock

import ipaddress, nmap

index='nmap_v3'

es_lock = Lock()
es = ElsSaveMap(index, index)

## ELASTICSEARCH index
NMAPPROCS=int(os.getenv('NMAPPROCS'))
HOSTSPROCS=int(os.getenv('HOSTSPROCS'))
# windows = 'windows'
# linux = 'linux'

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
                doc_type=index,
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

def main(options):

    shared_info['finalizar'] = False
    shared_info['sync'] = options['sync']
    #shared_info['force'] = options['force']

    if 'country' in options.keys():
        netobject = Network.objects.filter(
            local__activo = True,
            local__city__country = options['country']
        )
    elif 'flag' in options.keys():
        netobject = Network.objects.filter(
            local__activo = True,
            local__flag__flag = options['flag']
        )
    else:
        netobject = Network.objects.filter(local__activo = True)

    sub_net = CreateSubNetworks()
    for i in netobject:
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
        db.connections.close_all()

class Command(BaseCommand):
    help = 'make subnets from networks'
    def add_arguments(self, parser):
        parser.add_argument('--sync',
            action='store_true',
            dest='sync',
            default=False,
            help='Dont generate threads.')
        parser.add_argument('-c', '--country', required=False, \
                            help=u'country to search')
        parser.add_argument('-f', '--flag', required=False, \
                            help=u'country to search')
        parser.add_argument('-a', '--all', required=False, \
                            help=u'all networks')
        
    def handle(self, *args, **options):
        main(options)

manager = Manager()
hosts_shared_lists = manager.list([])
hosts_error_list = manager.list([])
nets_shared_lists = manager.list([])
shared_info = manager.dict()
