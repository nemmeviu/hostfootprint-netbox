#!/usr/bin/env python3
import urllib3, json, os, sys
http = urllib3.PoolManager()


# attribute = {
#     'map_type': '',
#     'ip': '',
#     'network': prefix,
#     'country': (esta en el parent),
#     'city': site.region.name,
#     'businessunit': netobject.local.flag.businessunit.businessunit,
#     'flag': site.tenant.name,
#     'local_id': netobject.local.local_id,
#     'local_address': netobject.local.local_address,
#     'local_desc': netobject.local.local_desc,
#     'geo_point': {
#         'lat': netobject.local.lat,
#         'lon': netobject.local.lon
#     }
# }


class NetboxAPI(object):
    '''
    NetboxAPI 
    '''
    def __init__(self):

        if os.getenv('NETBOX_API_URL') == None:
            self.netbox_api_url = 'http://netbox.cencosud.corp/api/'
        else:
            self.netbox_api_url = os.getenv('NETBOX_API_URL')            

        # path API URLs
        self.nb_api = {
            # RIR Aggregates            
            'rir': self.netbox_api_url + 'ipam/aggregates/',
            # IPAM Prefixes
            'prefix': self.netbox_api_url + 'ipam/prefixes/',

        }

    def json_import(self, nb_obj):
        '''
        Return json
        '''
        json_nb = json.loads(nb_obj.data)
        return(json_nb)

    def get_nb_api(self, nb_target, identity):
        '''
        Make the api request
        '''
        if identity == 'all':
            nb_target = self.nb_api[nb_target]
        else:
            nb_target = self.nb_api[nb_target] + '?parent=' + identity


        try:
            print(nb_target)
            nb_result = http.request('GET', nb_target)
        except:
            print('Fail to connect on: ' + nb_target)
            sys.exit(2)

        if nb_result.status == 200:
            return(self.json_import(nb_result))


    

    def get_countries(self):
        list_country = []
        all_agreggates = self.get_nb_api('rir', 'all')
        # print(countries)

        for agreggate in all_agreggates['results']:
            print(agreggate)
            country = {
                'network': agreggate['prefix'],
                'country': agreggate['rir']['name']
            }
            list_country.append(country)
        # print(list_country)
        return list_country



    def parse_prefixes(self):
        all_prefixes = self.get_nb_api('prefix', 'all')
        countries = self.get_countries()

        prefixes_list = []
        for country in countries:
            network = country['network']
            network = network.replace('/','%2F')
            prefixes_by_country = self.get_nb_api('prefix', network)

            for prefix in prefixes_by_country:
                # print(prefix)
            
            print(json.dumps(prefixes_by_country, indent=4, sort_keys=True))

            # for prefix in prefixes_by_country:
            #     # print(json.dumps(prefix , indent=4, sort_keys=True))
            #     # print(country['country'])
            #     prefixes_list.append(prefix)
            #     print(json.dumps(prefix, indent=4, sort_keys=True))



        # print(json.dumps(prefixes_list, indent=4, sort_keys=True))
        # for prefix in all_prefixes:
            


        # print(countries)
        



#/home/msantago/Documents/blacktourmaline/github/hostfootprint-netbox

test = NetboxAPI()

# print(test.get_nb_api('prefix'))
print(test.parse_prefixes())
