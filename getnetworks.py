#!/usr/bin/env python3
import urllib3, json, os, sys, argparse
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
            self.netbox_api_url = 'http://localhost/api/'
        else:
            self.netbox_api_url = os.getenv('NETBOX_API_URL')            

        # path API URLs
        self.nb_api = {
            # RIR Aggregates            
            'rir': self.netbox_api_url + 'ipam/aggregates/',
            'prefix': self.netbox_api_url + 'ipam/prefixes/',
            'site': self.netbox_api_url + 'dcim/sites/',
            'tenancy': self.netbox_api_url + 'tenancy/tenants/',
            'regions': self.netbox_api_url + 'dcim/regions/'
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
            if nb_target == 'prefix':
                nb_target = self.nb_api[nb_target] + '?parent=' + identity

            if nb_target in ('site', 'tenancy','regions'):
                nb_target = self.nb_api[nb_target] + identity

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

        for agreggate in all_agreggates['results']:
            country = {
                'network': agreggate['prefix'],
                'country': agreggate['rir']['name']
            }

            list_country.append(country)

        return list_country


    def parse_prefixes(self):
        countries = self.get_countries()
        network_valid = []
        network_invalid = []

        for country in countries:
            network = country['network']
            network = network.replace('/','%2F')

            # need FIX - no get inside loop
            prefixes_by_country = self.get_nb_api('prefix', network)

            for prefix in prefixes_by_country['results']:
                # print(json.dumps(prefix, indent=4, sort_keys=True))
                try:
                    site_id = prefix['site']['id']

                    # need FIX - get inside loop, inside loop - bad!!!
                    site = self.get_nb_api('site', str(site_id))
                    #
                    site_address = site['physical_address']
                    site_city = site['region']['name']
                    tenant_id = site['tenant']['id']

                    # need FIX - get inside loop, inside loop - bad!!!                    
                    tenant = self.get_nb_api('tenancy', str(tenant_id))
                    #
                    flag = tenant['name']
                    businessunit = tenant['group']['name']

                    # validate region
                    region_id = site['region']['id']
                    region = self.get_nb_api('regions', str(region_id))
                    site_country = region['parent']['name']

                    parsed = {
                        'country' : country['country'],
                        'network' : prefix['prefix'],
                        'site_name' : prefix['site']['name'],
                        'site_id' : site_id,
                        'site_address': site_address,
                        'site_city': site_city,
                        'flag': flag,
                        'businessunit':businessunit,
                    }

                    if prefix['vlan'] is not None:
                        parsed['vlan_id'] = prefix['vlan']['vid']
                        parsed['vlan_name'] = prefix['vlan']['name']
                    
                    if country['country'] == site_country:
                        network_valid.append(parsed)
                    else:
                        network_invalid.append(parsed)
                except:
                    pass

        print(json.dumps(network_valid, indent=4, sort_keys=True))
        print('===============================')            
        print(json.dumps(network_invalid, indent=4, sort_keys=True))


#/home/msantago/Documents/blacktourmaline/github/hostfootprint-netbox

#test = NetboxAPI()
#test.parse_prefixes()
# print(test.get_nb_api('prefix'))


parser = argparse.ArgumentParser(
    description='Netbox API -> pynmap -> elasticsearch',
    epilog='''
    hostfootprint with netbox, elasticsearch and nmap integration.
    \n
    Responsable: Millar Bravo.'''
)
parser.add_argument(
    '--country',
    dest='country',
    
)

args = parser.parse_args()
