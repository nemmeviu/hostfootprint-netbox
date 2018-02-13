#!/usr/bin/env python3
import urllib3, json, os, sys

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

    def conn(self, host, port):
        '''
        create initial connection with netbox
        '''
        if port == 443:
            self.netbox_api_url = 'https://%s' % host
            self.http = urllib3.HTTPSConnectionPool(
                host=host,
                port=port,
                maxsize=100
            )
        if port == 80:
            self.netbox_api_url = 'http://%s' % host
            self.http = urllib3.HTTPConnectionPool(
                host=host,
                port=port,
                maxsize=100
            )

        try:
            self.http.request('GET', self.netbox_api_url)
        except:
            print('Fail to connect on: ' + self.netbox_api_url)
            sys.exit(2)

        print('Sucessfull connection with: ' + self.netbox_api_url)
        
        # path API URLs
        self.nb_api = {
            'prefix': {
                'rir': self.netbox_api_url + '/api/ipam/rirs/',
                'agregates': self.netbox_api_url + '/api/ipam/agregates/',
                'prefix': self.netbox_api_url + '/api/ipam/prefixes/',
            },
            'tenant': {
                'sites': self.netbox_api_url + '/api/dcim/sites/',
                'tenancy': self.netbox_api_url + '/api/tenancy/tenants/',
                'regions': self.netbox_api_url + '/api/dcim/regions/'
            }
        }


    def make_nb_url(self, parent, search):
        '''
        make netbox url and generate self.url
        '''
        try:
            apiurl = self.nb_api[parent][search]
            print(apiurl)
        except:
            print(json.dumps(self.nb_api, indent=4, sort_keys=True))
            print('maybe the parent or search does not exist.')
            sys.exit(2)

        return(apiurl)

    def match(self, match, parent, search, limit=400):
        '''
        find and print objects on netbox api.
        '''
        match_result = {}

        apiurl = self.make_nb_url(parent, search)

        nb_target = '%s?%s=%s&limit=%s' % (apiurl, parent, match, limit)
        print('trying to find ' + match + ' with:')
        print(nb_target)
        
        try:
            nb_result = self.http.request('GET', nb_target)
            self.match_result = self.json_import(nb_result)
        except:
            print('Fail to connect on: ' + nb_target)
            self.match_result = {}

    def get_prefix_from_sites(self, limit=400):
        '''
        get list of prefixes inside object
        '''
        apiurl = self.make_nb_url('prefix', 'prefix')
        if 'results' in self.match_result.keys():
            results = self.match_result['results']
            for slug in results:
                nb_prefix = '%s?%s=%s&limit=%s' % (apiurl, 'site', slug['slug'], limit)
                nb_result = self.http.request('GET', nb_prefix)
                prefix = self.json_import(nb_result)
                slug['prefix'] = prefix

            
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

            self.get_prefix_from_sites()

            
    def output(self, output):
        '''
        make the output:
        screen or db
        '''
        if output == 'screen':
            pass
            print(json.dumps(self.match_result, indent=4, sort_keys=True))
        if output == 'db':
            print('elasticsearch save :)')
            print(self.match_result)
            
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
        nb_target = self.nb_api['prefix'][nb_target] + identify + '?limit=4000'
        print(nb_target)

        try:
            nb_result = self.http.request('GET', nb_target)
            print(nb_result.data)
        except:
            print('Fail to connect on: ' + nb_target)
            sys.exit(2)

        if nb_result.status == 200:
            return(self.json_import(nb_result))

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
        
        #countries = self.get_countries()
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

