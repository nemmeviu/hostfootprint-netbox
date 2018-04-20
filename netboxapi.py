#!/usr/bin/env python3
import urllib3, json, os, sys, datetime, time
from elasticsearch import Elasticsearch
from datetime import time as timeee
#from threading import Lock

class ElsSaveMap(object):
    def __init__(self, index, index_type):
        '''
        init global variables
        pass host to elasticsearch connect

        - create elasticsearch index
        '''
        self.client = Elasticsearch(
            hosts=[ os.getenv('ES_SERVER', '127.0.0.1') ]
        )

        self.index = index
        self.doc_type = index_type

        if self.index == 'netbox-dashboard':
            mapping = {
                "settings" : {
                    "number_of_shards" : 5,
                    "number_of_replicas" : 1,
                },
                "mappings": {
                    index_type:{
                        "properties": {
                            "g_flag": {
                                "index": "true", 
                                "type": "keyword"
                            },
                            "sites": {
	                        "type": "integer"
                            },
                            "prefix": {
                                "type": "integer"
                            },
                            "sites": {
                                "index": "true", 
                                "type": "keyword"
                            }
                        }
                    }
                }
            }
        else:
            mapping = {
                "settings" : {
                    "analysis": {
                        "normalizer": {
                            "my_normalizer": {
                                "type": "custom",
                                "char_filter": [],
                                "filter": ["lowercase", "asciifolding"]
                            }
                        }
                    },
                    "max_result_window": 35000,
                    "number_of_shards" : 5,
                    "number_of_replicas" : 1,
                },
                "mappings": {
                    index_type:{
                        "properties": {
                            "g_last_mod_date": {
	                        "type": "date",
	                        "format": "epoch_millis"
                            },
                            "g_country": {
                                "index": "true", 
                                "type": "keyword",
                                "normalizer": "my_normalizer"
                            },
                            "g_flag": {
                                "index": "true", 
                                "type": "keyword",
                                "normalizer": "my_normalizer"
                            },
                            "g_businessunit": {
                                "index": "true", 
                                "type": "keyword",
                                "normalizer": "my_normalizer"
                            },
                            "g_application": {
                                "index": "true", 
                                "type": "keyword",
                                "normalizer": "my_normalizer"
                            },
                            "g_kpi": {
	                        "type": "boolean"
                            },
                            "g_critical": {
	                        "type": "boolean"
                            },
                            "situation": {
                                "index": "true", 
                                "type": "keyword"
                            },
                            "physical_address": {
                                "index": "true", 
                                "type": "keyword",
                                "normalizer": "my_normalizer"
                            },
                            "city": {
                                "index": "true", 
                                "type": "keyword",
                                "normalizer": "my_normalizer"
                            },
                            "geo_location": {
	                        "type": "geo_point"
                            },
	                    "local_desc": {
	                        "index": "true", 
                                "type": "keyword",
                                "normalizer": "my_normalizer"
                            },
                            "map_type": {
                                "index": "true", 
                                "type": "keyword"
                            },
                            "local_id": {
                                "index": "true", 
                                "type": "keyword",
                                "normalizer": "my_normalizer"
                            },
	                    "local_address": {
	                        "index": "true", 
                                "type": "keyword",
                                "normalizer": "my_normalizer"
                            },
                            "sites": {
	                        "type": "integer"
                            },
                            "network": {
                                "index": "true", 
                                "type": "keyword"
                            },
                            "role": {
                                "index": "true", 
                                "type": "keyword"
                            },
                            "ip": {
                                "type": "ip"
                            },
	                    "hostname": {
	                        "index": "true", 
                                "type": "keyword",
                                "normalizer": "my_normalizer"                                
	                    },
	                    "parsed": {
                                "type": "short"
	                    },
	                    "exit_code": {
                                "type": "short"
	                    },
	                    "Caption": {
	                        "index": "true", 
                                "type": "keyword"
	                    },	    
	                    "FreePhysicalMemory": {
	                        "type": "long"
	                    },
	                    "TotalPhysicalMemory": {
	                        "type": "long"
	                    },
	                    "Model": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "CurrentTimeZone": {
	                        "type": "short"
	                    },
	                    "DaylightInEffect": {
	                        "type": "boolean"
	                    },
	                    "EnableDaylightSavingsTime": {
	                        "type": "boolean"
	                    },
	                    "NumberOfLogicalProcessors": {
	                        "type": "short"
	                    },
	                    "NumberOfProcessors": {
	                        "type": "short"
	                    },
	                    "ProcFamily": {
	                        "type": "short"
	                    },
	                    "ProcLoadPercentage": {
	                        "type": "short"
	                    },
	                    "ThermalState": {
	                        "type": "short"
	                    },
	                    "Vendor": {
	                        "index": "true",
                                "type": "keyword"
	                    },
	                    "err": {
	                        "index": "true",
                                "type": "keyword"
	                    },
	                    "ProcManufacturer": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "ProcName": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "Status": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "SystemType": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "IdentifyingNumber": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "LoadPercentage": {
	                        "type": "short"
	                    },
	                    "Manufacturer": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "Name": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "CSName": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "LastBootUpTime": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "ServicePackMajorVersion": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "HotFixID": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "OSArchitecture": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "Product": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "SerialNumber": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "UUID": {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "UserName": {
	                        "index": "true", 
                                "type": "keyword",
                                "normalizer": "my_normalizer"
	                    },
	                    "Version" : {
	                        "index": "true", 
                                "type": "keyword"
	                    },
	                    "Product_Name" : {
	                        "index": "true", 
                                "type": "keyword",
                                "normalizer": "my_normalizer"                                
	                    },
	                    "HotFixID" : {
	                        "index": "true", 
                                "type": "keyword",
	                    },
                            "DHCPServer": {
                                "index": "true", 
                                "type": "keyword"
	                    },
                            "IPAddress": {
                                "index": "true", 
                                "type": "keyword"
	                    },
                            "MACAddress": {
                                "index": "true", 
                                "type": "keyword"
	                    },
                            "ServiceName": {
                                "index": "true", 
                                "type": "keyword"
	                    }
                        }
                    }
                }
            }

        try:
            self.client.search(index=self.index)
        except:
            print('creating... %s' % self.index)
            new_index = self.client.indices.create(index=self.index, ignore=400, body=mapping)
            print(new_index)

    def check_time(self):
        ''' sub_net = ip_net.subnets(new_prefix=24)
        import datetimeist(sub_net)
        20:00 - 06:00 = ip-20-06
        06:00 - 20:00 = ip-06-20
        return( [ ip_net ])
        return('xx-xx')
        '''
        datenow = datetime.datetime.now()
        timenow = datenow.time()

        start = timeee(6, 0, 0)
        end = timeee(20, 0, 0)

        timestr = datenow.strftime("%y%m%d")

        if timenow >= start and timenow < end:
            return(timestr + '-06-20')
        else:
            return(timestr + '-20-06')

    def es_save(self, map_type, host, n_object):
        
        attribute = {}

        attribute['g_kpi'] = False
        attribute['g_critical'] = False
        try:
            attribute['map_type'] = map_type
        except:
            pass
        try:
            attribute['ip'] = host
        except:
            pass
        try:
            attribute['role'] = n_object['role']
        except:
            pass
        try:
            attribute['network'] = n_object['prefix']
        except:
            pass
        try:
            attribute['g_country'] = n_object['g_country']
        except:
            pass
        try:
            attribute['g_flag'] = n_object['g_flag']
        except:
            pass
        try:            
            attribute['g_businessunit'] = n_object['g_businessunit']
        except:
            pass
        try:
            attribute['local_id'] = n_object['local_id']
        except:
            pass
        try:
            attribute['physical_address'] = n_object['physical_address']
        except:
            pass
        try:
            attribute['local_desc'] = n_object['comments']
        except:
            pass
        
        try:
            attribute['geo_location'] = {
                'lat': n_object['custom_fields']['latitud'],
                'lon': n_object['custom_fields']['latitud']
            }
        except:
            pass

        normalize = ''.join(c.lower() for c in host if not c.isspace())
        today = datetime.date.today().strftime("%m%d%Y")

        data = datetime.datetime.now()
        date_els = int( data.timestamp() * 1000 )

        attribute['g_last_mod_date'] = date_els

        # old 1['finalizar'] = False
        #_id=(normalize + '-' + today)
        # old 2o['force'] = options['force']
        #_id=(normalize + '-' + str(date_els))

        _id=(normalize + '-' + self.check_time())

        try:
            response = self.client.index(
                index=self.index,
                id=_id,
                doc_type=self.doc_type,
                body=attribute
            )
        except:
            print('fail in _id: %s' % _id )

    def save_dashboard(self, output):
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
        '''
        init basic variables
        self.version and self.g_nb

        '''
        self.version = "v0.1"

        self.g_nb = {
            'tenant': False,
            'country': {}
        }

    def conn(self, host, port):
        '''
        - create initial connection with netbox root URL
        - create self.nb_api dictonary that have path to all netbox api calls

        '''
        if port == 443:
            self.netbox_api_url = 'https://%s' % host
            self.http = urllib3.HTTPSConnectionPool(
                host=host,
                port=port,
                maxsize=2000
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
        create netbox url based on self.nb_api dict and
        generate self.url
        '''
        try:
            apiurl = self.nb_api[parent][match][search]
        except:
            print(json.dumps(self.nb_api, indent=4, sort_keys=True))
            print('maybe the parent or search does not exist.')
            print(self.nb_api[parent][match][search])
            sys.exit(2)
        print('------------- apiurl: %s' % apiurl)
        return(apiurl)

    

    def match(self, match, parent, search, limit=1000):
        '''
        find and print objects on netbox api.
        '''
        match_result = {}

        print('''------- Params:
        match_type: %s
        match: %s
        parent: %s
        search: %s''' %
              (self.match_type, match, parent, search)
        )
        
        apiurl = self.make_nb_url(parent, self.match_type, search)
        print('api-url: {}'.format(apiurl))
        
        if self.match_type == 'all':
            nb_target = '%s?limit=%s' % (apiurl, limit)
        else:
            nb_target = '%s%s&limit=%s' % (apiurl, match, limit)
            
        try:
            nb_result = self.http.request('GET', nb_target)
            self.match_result = self.json_import(nb_result)
            #print(self.match_result['results'])
            print('Successfull find %s' %  nb_target)
        except:
            print('Fail to connect on: ' + nb_target)
            self.match_result = {}

    def get_prefix_from_search(self, limit=400,role=False):
        '''
        get list of prefixes inside object
        '''
        print('get_prefix_from_search')
        apiurl = self.make_nb_url('prefix', 'match', 'prefix')
        print(apiurl)
        if 'results' in self.match_result.keys():
            for slug in self.match_result['results']:
                if role:
                    nb_prefix = '%s%s=%s&limit=%s&role=%s' % (
                        apiurl,
                        self.search_string,
                        slug['slug'],
                        limit,
                        role)
                    print(nb_prefix)
                else:
                    nb_prefix = '%s%s=%s&limit=%s' % (
                        apiurl,
                        self.search_string,
                        slug['slug'],
                        limit)
                    print('sin role: %s' % nb_prefix)
                nb_result = self.http.request('GET', nb_prefix)
                prefix = self.json_import(nb_result)
                #print('prefix: %s' % prefix)
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
        1 -  first def. 
        receive dict with required params:
        - search_type
        - parent
        - search

        turn all thinks real!

        '''
        print('search: %s' % kwargs['search'])
        self.search_string = kwargs['search']
        
        self.match_type = kwargs['match_type']

        ## principal object!!
        # create self.match_result with results
        self.match(
            kwargs['match'],
            kwargs['parent'],
            kwargs['search'],
        )

        if kwargs['search_type'] != 'dashboard':
            
            # add prefix inside sites objects
            if 'role' in kwargs.keys():
                self.get_prefix_from_search(role=kwargs['role'])
            else:
                self.get_prefix_from_search()
        else:
            print(
                json.dumps(
                    self.match_result['results'][4],
                    indent=4,
                    sort_keys=True
                )
            )
            
        #self.get_sites_from_search()
        
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

        return(self.g_nb)


    def output(self, output):
        '''
        make the output:
        screen or db
        '''
        if output == 'screen':
            print(json.dumps(self.match_result, indent=4, sort_keys=True))
        if output == 'db':
            '''prepair object to nmap process'''
            nmap_list = []
            prefixcontrol = []     
            for nb_obj in self.match_result['results']:
                nmap_object = {}                
                print(nb_obj)
                print(nb_obj.keys())
                print(nb_obj['name'])
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
                    for prefixtmp in nb_obj['prefix']['results']:
                        if prefixtmp['prefix'] not in prefixcontrol:
                            #print('new prefix control: %s' % prefixtmp['prefix'])
                            prefixcontrol.append(prefixtmp['prefix'])
                            prefix_obj = dict(nmap_object)
                            prefix_obj['prefix'] = prefixtmp['prefix']
                            prefix_obj['role'] = prefixtmp['role']['name']
                            nmap_list.append(prefix_obj)                        
                except:
                    prefix_obj['status'] = 1
                    print('fora')
                    # controle ... dashboard

                    #print(nmap_list)
                    #print(json.dumps(prefix_obj, indent=4, sort_keys=True))
                
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

