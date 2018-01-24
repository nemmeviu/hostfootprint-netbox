#!/usr/bin/env python3
import urllib3, json, os, sys
http = urllib3.PoolManager()

class NetboxAPI(object):
    '''
    NetboxAPI 
    '''
    def __init__(self):

        if os.getenv('NETBOX_API_URL') == None:
            self.netbox_api_url = 'http://localhost/api/'
        else:
            self.netbox_api_url = os.getenv('NETBOX_API_URL')            

        # path API URLs
        self.nb_api = {
            # RIR Aggregates            
            'rir': self.netbox_api_url + 'ipam/aggregates/',
            # IPAM Prefixes
            'prefix': self.netbox_api_url + 'ipam/prefixes/'
        }

    def json_import(self, nb_obj):
        '''
        Return json
        '''
        
        json_nb = json.loads(nb_obj.data)
        return(json_nb)

    def get_nb_api(self, nb_target):
        '''
        Make the api request
        '''

        nb_target = self.nb_api[nb_target]

        try:
            print(nb_target)
            nb_result = http.request('GET', nb_target)
        except:
            print('Fail to connect on: ' + nb_target)
            sys.exit(2)

        if nb_result.status == 200:
            return(self.json_import(nb_result))

#/home/msantago/Documents/blacktourmaline/github/hostfootprint-netbox

test = NetboxAPI()

print(test.get_nb_api('prefix'))
