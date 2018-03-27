FROM python:3

RUN mkdir /opt/hostfootprint-netbox

RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \    
    apt-get install -y curl nmap

COPY requirements.txt /opt/hostfootprint-netbox/requirements.txt
RUN pip install -r /opt/hostfootprint-netbox/requirements.txt

COPY netboxapi.py /opt/hostfootprint-netbox/netboxapi.py
COPY dashboard.py /opt/hostfootprint-netbox/dashboard.py
COPY getnetworks.py /opt/hostfootprint-netbox/getnetworks.py
COPY index /opt/hostfootprint-netbox/index

WORKDIR /opt/hostfootprint-netbox
