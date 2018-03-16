#!/usr/bin/env python3
import urllib3, json, os, sys
from elasticsearch import Elasticsearch

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

        self.g_nb = {
            'tenant': False,
            'country': {}
        }

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
        else:
            self.netbox_api_url = 'http://%s:%s' % (host, port)
            print(self.netbox_api_url)
            self.http = urllib3.HTTPConnectionPool(
                host=host,
                port=port,
                maxsize=2000
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
                'match': {
                    'rir': self.netbox_api_url + '/api/ipam/rirs/',
                    'agregates': self.netbox_api_url + '/api/ipam/agregates/',
                    'prefix': self.netbox_api_url + '/api/ipam/prefixes/?',
                },
                'all': {
                    'rir': self.netbox_api_url + '/api/ipam/rirs/',
                    'agregates': self.netbox_api_url + '/api/ipam/agregates/',
                    'prefix': self.netbox_api_url + '/api/ipam/prefixes/',
                }
            },
            'tenant': {
                'match': {
                    'site': self.netbox_api_url + '/api/dcim/sites/?tenant=',
                    'tenant': self.netbox_api_url + '/api/tenancy/tenants/?name=',
                    'regions': self.netbox_api_url + '/api/dcim/regions/?slug='
                },
                'all': {
                    'site': self.netbox_api_url + '/api/dcim/sites/',
                    'tenant': self.netbox_api_url + '/api/tenancy/tenants/',
                    'regions': self.netbox_api_url + '/api/dcim/regions/'
                }
            },
            'site': {
                'match': {
                    'site': self.netbox_api_url + '/api/dcim/sites/?slug=',
                },
                'all': {
                    'site': self.netbox_api_url + '/api/dcim/sites/',
                }
            }
        }


    def make_nb_url(self, parent, match, search):
        '''
        make netbox url and generate self.url
        '''
        try:
            apiurl = self.nb_api[parent][match][search]
        except:
            print(json.dumps(self.nb_api, indent=4, sort_keys=True))
            print('maybe the parent or search does not exist.')
            print(self.nb_api[parent][match][search])
            sys.exit(2)
        return(apiurl)

    def match(self, match, parent, search, limit=1000):
        '''
        find and print objects on netbox api.
        '''
        match_result = {}

        print('match_type: %s, match: %s, parent: %s, search: %s' %
              (self.match_type, match, parent, search)
        )
        
        apiurl = self.make_nb_url(parent, self.match_type, search)

        if match is False:
            nb_target = '%s?limit=%s' % (apiurl, limit)
        else:
            nb_target = '%s%s&limit=%s' % (apiurl, match, limit)
            
        print('Trying to find %s' %  nb_target)
        
        try:
            nb_result = self.http.request('GET', nb_target)
            self.match_result = self.json_import(nb_result)
        except:
            print('Fail to connect on: ' + nb_target)
            self.match_result = {}

    def get_prefix_from_search(self, limit=400,role=False):
        '''
        get list of prefixes inside object
        '''
        apiurl = self.make_nb_url('prefix', 'match', 'prefix')
        if 'results' in self.match_result.keys():
            results = self.match_result['results']
            for slug in results:
                if role:
                    nb_prefix = '%s%s=%s&limit=%s&role=%s' % (apiurl, self.search_string, slug['slug'], limit, role)
                else:
                    nb_prefix = '%s%s=%s&limit=%s' % (apiurl, self.search_string, slug['slug'], limit)
                nb_result = self.http.request('GET', nb_prefix)
                prefix = self.json_import(nb_result)
                slug['prefix'] = prefix
                
    def get_sites_from_search(self, limit=1000):
        '''
        get list of prefixes inside object
        '''
        apiurl = self.make_nb_url('tenant', 'match', 'site')
        if 'results' in self.match_result.keys():
            results = self.match_result['results']
            for slug in results:
                nb_prefix = '%s%s&limit=%s' % (apiurl, slug['slug'], limit)
                nb_result = self.http.request('GET', nb_prefix)
                prefix = self.json_import(nb_result)
                slug['sites'] = prefix
                
    def search(self, **kwargs):
        '''
        turn all thinks real!

        '''
        print('search: %s' % kwargs['search'])


        self.match_type = kwargs['match_type']
        self.search_string = kwargs['search']

        # create self.match_result with results
        self.match(
            kwargs['match'],
            kwargs['parent'],
            kwargs['search'],
        )

        # add prefix inside sites objects
        if 'role' in kwargs.keys():
            self.get_prefix_from_search(role=kwargs['role'])
        else:
            self.get_prefix_from_search()
            
        self.get_sites_from_search()
        
        try:
            # tenant if tenant
            #if kwargs['parent'] in [ 'tenant', 'site' ]:
            if kwargs['parent'] in [ 'site' ]:                
                self.g_nb['tenant'] = self.make_nb_url('tenant', 'tenant')
                self.g_nb['tenant'] = '%s%s&limit=%s' % (self.g_nb['tenant'], self.match_result['results'][0]['name'], 1)
                self.g_nb['tenant'] = self.http.request('GET', self.g_nb['tenant'])
                #print('url:')
                #print(self.g_nb['tenant'])
                self.g_nb['tenant'] = self.json_import(self.g_nb['tenant'])
                self.g_nb['tenant'] = self.g_nb['tenant']['results'][0]['group']['name']
        except:
            print('review your search:')                
            print(self.g_nb['tenant'])
            print(sys.exit(2))


    def save_dashboard(self, output, es_server=False, es_port=False):
        '''
        make the output:
        screen or db
        '''
        
        if output == 'screen':
            print(json.dumps(self.match_result, indent=4, sort_keys=True))
        if output == 'db':
            
            #try:
            es = Elasticsearch('127.0.0.1')
                #es = Elasticsearch(es_server)
                #es.info()
            #except:
            #    print('fail to connect')
            #    sys.exit(2)
            
            INDEX='netbox-dashboard'

            es_obj = {}
            for i in self.match_result['results']:
                es_obj['g_flag'] = i['name']
                es_obj['prefix'] = i['prefix']['count']
                es_obj['sites'] = i['sites']['count']
                _id = es_obj['g_flag']                
                es.index(index=INDEX, doc_type='infra', id=_id, body=es_obj)

    def output(self, output):
        '''
        make the output:
        screen or db
        '''
        if output == 'screen':
            print(json.dumps(self.match_result, indent=4, sort_keys=True))
        if output == 'db':
            "prepair object to nmap process"
            nmap_list = []
            for nb_obj in self.match_result['results']:
                nmap_object = {}                

                # only for sites search =( .. mvp
                nmap_object['g_flag'] = nb_obj['tenant']['name']
                nmap_object['local_id'] = nb_obj['name']

                try:
                    nmap_object['situation'] = nb_obj['custon_fields']['situation']
                except:
                    pass
                
                try:
                    nmap_object['physical_address'] = nb_obj['physical_address']
                except:
                    pass
                try:
                    nmap_object['city'] = nb_obj['region']['name']
                except:
                    pass
                
                nmap_object['g_businessunit'] = self.g_nb['tenant']

                # get country ...
                # inside loop because the country can change
                try:
                    if nmap_object['city'] not in self.g_nb['country'].keys():
                        country = self.make_nb_url('tenant', 'match', 'regions')
                        country = '%s%s&limit=%s' % (country, nb_obj['region']['slug'], 100)
                        country = self.http.request('GET', country)
                        country = self.json_import(country)
                        print(country)
                        country = country['results'][0]['parent']['name']
                        #self.g_nb['country'][nmap_object['city']] = country
                        nmap_object['g_country'] = country
                except:
                    pass

                try:
                    nmap_object['prefix'] = nb_obj['prefix']['results'][0]['prefix']
                    nmap_object['status'] = 0
                except:
                    nmap_object['status'] = 1

                nmap_list.append(nmap_object)
                print(json.dumps(nmap_object, indent=4, sort_keys=True))
                
            return(nmap_list)
            #print('elasticsearch save :)')

    def output_prefix(self, output):
        '''
        make the output:
        screen or db
        '''
        if output == 'screen':
            print(json.dumps(self.match_result, indent=4, sort_keys=True))
        if output == 'db':
            ''' prepair object to nmap process '''
            nmap_object = {}
            for nb_obj in self.match_result['results']:
                
                nmap_object['g_flag'] = nb_obj['name']
                nmap_object['location'] = nb_obj['name']

                try:
                    nmap_object['geo_location'] 
                    nmap_object['geo_location'] = {
                        'lat': nb_obj['custom_fields']['latitud'],
                        'lon': nb_obj['custom_fields']['longitud']
                    }
                except:
                    pass
                
                try:
                    nmap_object['location'] = nb_obj['custom_fields']
                except:
                    pass
                try:
                    nmap_object['local_address'] = nb_obj['physical_address']
                except:
                    pass
                try:
                    nmap_object['city'] = nb_obj['region']['name']
                except:
                    pass
                nmap_object['g_businessunit'] = self.g_nb['tenant']

                try:
                    # get country ...
                    # inside loop because the country can change
                    if nmap_object['city'] not in self.g_nb['country'].keys():
                        country = self.make_nb_url('tenant', 'regions')
                        country = '%s%s&limit=%s' % (country, nb_obj['region']['slug'], 1)
                        country = self.http.request('GET', country)
                        country = self.json_import(country)
                        country = country['results'][0]['parent']['name']
                        self.g_nb['country'][nmap_object['city']] = country
                        nmap_object['g_country'] = country
                except:
                    pass

                print(json.dumps(nmap_object, indent=4, sort_keys=True))
            print('elasticsearch save :)')

    def json_import(self, nb_obj):
        '''
        Return json
        '''
        try: 
            json_nb = json.loads(nb_obj.data)
            return(json_nb)
        except:
            print('fail to get data from this object')
            print(nb_obj)
            sys.exit(2)

    # def get_nb_api(self, nb_target, identify):
    #     '''
    #     Make the api request
    #     '''
    #     nb_target = self.nb_api['prefix'][nb_target] + identify + '?limit=4000'
    #     print(nb_target)

    #     try:
    #         nb_result = self.http.request('GET', nb_target)
    #         print(nb_result.data)
    #     except:
    #         print('Fail to connect on: ' + nb_target)
    #         sys.exit(2)

    #     if nb_result.status == 200:
    #         return(self.json_import(nb_result))

    # def get_countries(self):

    #     try:
    #         rirs = self.get_nb_api('rir', '?name=' + self.country)
    #     except:
    #         rirs = self.get_nb_api('rir', '')            

    #     self.netbox_obj = rirs
    #     #return(rirs)

    #     #all_agreggates = self.get_nb_api('rir')

    #     #for agreggate in all_agreggates['results']:
    #     #    country = {
    #     #        'network': agreggate['prefix'],
    #     #        'country': agreggate['rir']['name']
    #     #    }
    #     #    list_country.append(country)
    #     #return list_country

    # def parse_prefixes(self):
        
    #     #countries = self.get_countries()
    #     networks = []
    #     #network_valid = []
    #     #network_invalid = []

    #     for country in countries:
    #         network = country['network']
    #         network = network.replace('/','%2F')

    #         # need FIX - no get inside loop
    #         prefixes_by_country = self.get_nb_api('prefix', network)

    #         for prefix in prefixes_by_country['results']:
    #             # print(json.dumps(prefix, indent=4, sort_keys=True))
    #             try:
    #                 site_id = prefix['site']['id']

    #                 # need FIX - get inside loop, inside loop - bad!!!
    #                 site = self.get_nb_api('site', str(site_id))
    #                 #
    #                 site_address = site['physical_address']
    #                 site_city = site['region']['name']
    #                 tenant_id = site['tenant']['id']

    #                 # need FIX - get inside loop, inside loop - bad!!!
    #                 tenant = self.get_nb_api('tenant', str(tenant_id))
    #                 #
    #                 flag = tenant['name']
    #                 businessunit = tenant['group']['name']

    #                 # validate region
    #                 region_id = site['region']['id']
    #                 region = self.get_nb_api('regions', str(region_id))
    #                 site_country = region['parent']['name']

    #                 parsed = {
    #                     'country' : country['country'],
    #                     'network' : prefix['prefix'],
    #                     'site_name' : prefix['site']['name'],
    #                     'site_id' : site_id,
    #                     'site_address': site_address,
    #                     'site_city': site_city,
    #                     'flag': flag,
    #                     'businessunit':businessunit,
    #                 }

    #                 if prefix['vlan'] is not None:
    #                     parsed['vlan_id'] = prefix['vlan']['vid']
    #                     parsed['vlan_name'] = prefix['vlan']['name']
                    
    #                 #if country['country'] == site_country:
    #                 #    network_valid.append(parsed)
    #                 #else:
    #                 #    network_invalid.append(parsed)
    #                 network.append(parsed)                    
    #             except:
    #                 pass

    #     return(network)
    #     print(json.dumps(network, indent=4, sort_keys=True))
    #     #print(json.dumps(network_valid, indent=4, sort_keys=True))
    #     #print('===============================')            
    #     #print(json.dumps(network_invalid, indent=4, sort_keys=True))

    # def base_scan(self, prefix, sites):
    #     print(len(prefix))
    #     print(len(sites))        
    #     #print(prefix)
    #     #for x in prefix:
    #     #    if x['site'] is not None:
    #     #        print(x['site'])
    #     #        print('looping 1')
    #     #        for k in sites:
    #     #            if x['site']['name'] == k['name']:
    #     #                print(k['id'])
    #     #                print(x['site']['id'])
    #        #print(sites['id'][x['sites']['id']])
    #     #pass

