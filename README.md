# hostfootprint-netbox

Map networks based on Netbox IPAM Project.

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

| ENV Vars     | value default  | description                           |
|--------------|:--------------:|:-------------------------------------:|
| ES_SERVER    | 127.0.0.1      | Elasticsearch Server IP/DNS name      |   
| ES_INDEX     | nmap	        | Indice elasticsearch                  |
| NMAPPROCS    | 20             | Number of simultaneos nmaps           |
| HOSTSPROCS   | 2              | Number of simultaneos wmic procs      |
| SYNC         | 1              | multiprocessing active or not: 1 or 0 |

#### usage

##### dashboard

Save all tenants totals counts
```
./dashboard.py --parent tenant --search tenant --output db --host netbox.corp --port 8008
```

##### hostfootprint

Get all tenants
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
