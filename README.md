# hostfootprint-netbox

Map networks based on Netbox IPAM Project.

Usage:
```
$ pip3 install -r requirements.txt
$ python3
>>> from netboxapi import NetboxAPI
>>> nb = NetboxAPI()
>>> nb.version
'v0.1'
>>> exit()
$ ./getnetworks.py --parent tenant --output screen \
 --url http://netbox.domain.com/api/ --search sites --match ti
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
