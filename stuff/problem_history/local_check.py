#!/usr/bin/env python3
import socket
import json

sockets = [
    "/omd/sites/mon/tmp/run/live",
    "/omd/sites/mon/tmp/run/liveproxy/mon2",
]

def prepare_request(what):
    data = "\n".join(what)
    data += "\n"
    data += "\n"
    try:
        return bytes(str(data), 'utf-8')
    except TypeError:
        return str(data)

def call(peer, request):
    try:
        if len(peer) == 2:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(peer)
        s.send(request)
        s.shutdown(socket.SHUT_WR)
        rawdata = s.makefile().read()
        if not rawdata:
            return []
        cleanup = rawdata.split('\n')
        del cleanup[0]
        cleaned = "\n".join(cleanup)
        data = json.loads(cleaned)
        return [dict(zip(data[0], value)) for value in data[1:]]
    except:
        raise
    finally:
        s.close()


filter_services = [
    'GET services',
    'ResponseHeader: fixed16',
    'Columns: description',
    'Filter: state = 2',
    'OutputFormat: json',
    'ColumnHeaders: on',
    'KeepAlive: on',
]

filter_hosts = [
    'GET hosts',
    'ResponseHeader: fixed16',
    'Columns: name',
    'Filter: state = 1',
    'OutputFormat: json',
    'ColumnHeaders: on',
    'KeepAlive: on',
]

num_services = 0
num_hosts = 0

for peer in sockets:
    services = call(peer, prepare_request(filter_services))
    num_services += len(services)
    
    hosts = call(peer, prepare_request(filter_hosts))
    num_hosts += len(hosts)

print("0 dashboard services={0};hosts={1} Found Errors on {1} Hosts and {0} Services".format(num_services, num_hosts))
