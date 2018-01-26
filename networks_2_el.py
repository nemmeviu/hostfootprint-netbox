#encoding=utf8
import sys
#from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from general.models import *
from networks.models import *

def main(options):

    # total tiendas
    all_locals = Local.objects.all()

    for x in all_locals:

        network = Network.objects.filter(
            local = x
        )

        network_list = []
        for net in network:
            network_list.append(net.network)

        if len(network_list) > 0:
            print(network_list)

            #body = {
            #    "script" : "ctx._source.network = network_list"
            #}
            body = {
                "doc":{
                    "network": network_list
                }
            }

            x_obj = {
                'local_id': x.local_id,
            }
            el = ElsSave('locals')
            el.els_update(x_obj, body)

class Command(BaseCommand):
    help = 'create global object and save on elasticsearch'
    def add_arguments(self, parser):
        parser.add_argument('-a', '--action', required=False, \
                            help=u'save or console')

    def handle(self, *args, **options):
        main(options)
