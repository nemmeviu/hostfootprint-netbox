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
        self.version = "v0.1"

    def conn(self, boxurl):
        '''
        create initial connection with netbox
        '''
        self.netbox_api_url = boxurl

        try:
            http.request('GET', self.netbox_api_url)
        except:
            print('Fail to connect on: ' + self.netbox_api_url)
            sys.exit(2)

        print('Sucessfull connection with: ' + self.netbox_api_url)
        
        # path API URLs
        self.nb_api = {
            'prefix': {
                'rir': self.netbox_api_url + 'ipam/rirs/',
                'agregates': self.netbox_api_url + 'ipam/agregates/',
                'prefix': self.netbox_api_url + 'ipam/prefixes/',
            },
            'tenant': {
                'sites': self.netbox_api_url + 'dcim/sites/',
                'tenancy': self.netbox_api_url + 'tenancy/tenants/',
                'regions': self.netbox_api_url + 'dcim/regions/'
            }
        }

    def match(self, match, parent, search, limit=400):
        '''
        find and print objects on netbox api.
        '''
        match_result = {}

        try:
            apiurls = self.nb_api[parent][search]
            print(apiurls)
        except:
            print(json.dumps(self.nb_api, indent=4, sort_keys=True))
            print('maybe the parent or search does not exist.')
            sys.exit(2)

        nb_target = '%s?%s=%s&limit=%s' % (apiurls, parent, match, limit)
        print('trying to find ' + match + ' with:')
        print(nb_target)
        
        #for box in apiurls.keys():

        try:
            nb_result = http.request('GET', nb_target)
            match_result = self.json_import(nb_result)
        except:
            print('Fail to connect on: ' + nb_target)

        print(json.dumps(match_result, indent=4, sort_keys=True))
            
    def in_action(self, **kwargs):
        '''
        turn all thinks real!
        '''
        if 'match' in kwargs.keys():
            self.match(
                kwargs['match'],
                kwargs['parent'],
                kwargs['search'],
            )
            
    def json_import(self, nb_obj):
        '''
        Return json
        '''
        json_nb = json.loads(nb_obj.data)
        return(json_nb)

    def get_nb_api(self, nb_target, identify):
        '''
        Make the api request
        '''

        nb_target = self.nb_api[nb_target] + identify + '?limit=4000'

        try:
            nb_result = http.request('GET', nb_target)
        except:
            print('Fail to connect on: ' + nb_target)
            sys.exit(2)

        if nb_result.status == 200:
            return(self.json_import(nb_result))

        #if tenant_list == None:
        #    print('nao tem nada naoo')
        #    nb_target = self.nb_api[nb_target] + identify + '?limit=4000'
        #else:
        #    if nb_target == 'prefix':
        #        nb_target = self.nb_api[nb_target] + '?parent=' + identity + '&limit=4000'
        #
        #    if nb_target in ('site', 'tenancy','regions'):
        #        nb_target = self.nb_api[nb_target] + identity + '&limit=4000'
        
    def get_countries(self):

        try:
            rirs = self.get_nb_api('rir', '?name=' + self.country)
        except:
            rirs = self.get_nb_api('rir', '')            

        self.netbox_obj = rirs
        #return(rirs)

        #all_agreggates = self.get_nb_api('rir')

        #for agreggate in all_agreggates['results']:
        #    country = {
        #        'network': agreggate['prefix'],
        #        'country': agreggate['rir']['name']
        #    }
        #    list_country.append(country)
        #return list_country

    def parse_prefixes(self):
        countries = self.get_countries()
        networks = []
        #network_valid = []
        #network_invalid = []

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
                    
                    #if country['country'] == site_country:
                    #    network_valid.append(parsed)
                    #else:
                    #    network_invalid.append(parsed)
                    network.append(parsed)                    
                except:
                    pass

        return(network)
        print(json.dumps(network, indent=4, sort_keys=True))
        #print(json.dumps(network_valid, indent=4, sort_keys=True))
        #print('===============================')            
        #print(json.dumps(network_invalid, indent=4, sort_keys=True))

    def base_scan(self, prefix, sites):
        print(len(prefix))
        print(len(sites))        
        #print(prefix)
        #for x in prefix:
        #    if x['site'] is not None:
        #        print(x['site'])
        #        print('looping 1')
        #        for k in sites:
        #            if x['site']['name'] == k['name']:
        #                print(k['id'])
        #                print(x['site']['id'])
           #print(sites['id'][x['sites']['id']])
        #pass

