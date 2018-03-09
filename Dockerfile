FROM python:3

RUN mkdir /opt/hostfootprint-netbox

COPY netboxapi.py /opt/hostfootprint-netbox/netboxapi.py
COPY dashboard.py /opt/hostfootprint-netbox/dashboard.py
COPY requirements.txt /opt/hostfootprint-netbox/requirements.txt
COPY index /opt/hostfootprint-netbox/index

RUN set -ex; \
    apt-get update; \
    apt-get install curl

RUN pip install -r /opt/hostfootprint-netbox/requirements.txt

WORKDIR /opt/hostfootprint-netbox
