hostfootprint-netbox
======================

* Map networks based on Netbox IPAM Project. 
* Generate one dashboard with netbox register information

Basicaly search for tenants or sites inside netbox and get all prefixes.

Execute on clean nmap on the networks, and send the result to elasticsearch db.

Installation:
```
$ pip3 install -r requirements.txt
$ python3
>>> from netboxapi import NetboxAPI
>>> nb = NetboxAPI()
>>> nb.version
'v0.1'
>>> exit()
```

#### usage
```
$ ./getnetboxdata.py  -h
usage: getnetboxdata.py [-h] --host HOST --port PORT --type TYPE --output OUTPUT
                        [--role ROLE] [--parent PARENT] [--country COUNTRY]
                        [--tenant [TENANT [TENANT ...]]]
                        [--tenantgroup TENANTGROUP] --search SEARCH
                        [--match MATCH] [--esserver ES_SERVER] [--esport ES_PORT]

Map networks based on Netbox IPAM Project. Generate one dashboard with netbox
register information. Use elasticsearch in all modes

optional arguments:
  -h, --help            show this help message and exit
  --host HOST, -H HOST  The netbox url. Ex: netbox.domain.com
  --port PORT, -p PORT  ex: 80
  --type TYPE, -t TYPE  values: dashboard|prefix
  --output OUTPUT, -o OUTPUT
                        output: screen or db
  --role ROLE, -r ROLE  VLAN/Prefix Roles
  --parent PARENT, -P PARENT
                        parent: --parent tenent
  --country COUNTRY, -C COUNTRY
                        Country: --country China
  --tenant [TENANT [TENANT ...]], -T [TENANT [TENANT ...]]
                        tenant with spaces: --tenant jumbo
  --tenantgroup TENANTGROUP, -tg TENANTGROUP
                        tenant group: --tenantgroup super-marketing
  --search SEARCH, -s SEARCH
                        search: --search sites|tenacy|regions
  --match MATCH, -m MATCH
                        Find and Print
  --esserver ES_SERVER, -es ES_SERVER
                        elasticsearch_server
  --esport ES_PORT, -ep ES_PORT
                        elasticsearch_port

Making inventory about your network!
```

### required argparses

* ti (tenent)
* sites (type of search)
* tenant (type of parent)
* screen (output in console)

use pynmap to map hosts on networks.
* ports

send the result of on elasticsearch database
* mapping sample

Generate bashboard of day by day evolution

Objective

Difference

#### Variables for hostfootprint

| ENV Vars      | value default  | description                            |
|--------------:|:--------------:|:--------------------------------------:|
| ES_SERVER     | 127.0.0.1      | Elasticsearch Server IP/DNS name       |   
| ES_INDEX      | nmap	         | Indice elasticsearch                   |
| ES_INDEX_TYPE | nmap	         | Type object inside index elasticsearch |
| NMAPPROCS     | 20             | Number of simultaneos nmaps            |
| HOSTSPROCS    | 2              | Number of simultaneos wmic procs       |
| SYNC          | 1              | multiprocessing active or not: 1 or 0  |


##### dashboard

Save all tenants totals counts
```
./dashboard.py --parent tenant --search tenant --output db --host netbox.corp --port 8008
```

#### hostfootprint

##### Get all tenants

Get all tenants on screen
```
./getnetworks.py --parent tenant --search tenant --output screen --host netbox.localhost.corp --port 80
```

Send all sites on of some tenant to database
```
./getnetworks.py --parent tenant --search tenant --output screen \n
  --host netbox.localhost.corp --port 80 
```

Get list of sites by tenant
```
./getnetworks.py --parent tenant --search sites --output screen \n
  --host netbox.localhost.corp --port 80 --match tenant-slug
```

Get all prefixes with site-summarized role
```
./getnetworks.py  --parent tenant --search site --output db  --host xxx.xxx.xxx.xxx --port 8008 --match ti --role site-summarized
```

Save prefixes in elasticsearch
```
./getnetworks.py  --parent tenant --search site --output db  --host netbox.company.corp --port 80 --match flag_name --role site-summarized
```


* fix search command line
* fix dashboard netbox
* fix g_country
