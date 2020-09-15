#!/usr/bin/env python3
from mk_livestatus import Socket

sockets = [
    "/omd/sites/mon/tmp/run/live",
]

num_services = 0
num_hosts = 0
for socket in sockets:
    ls = Socket(socket)
    num_hosts += len(ls.hosts.columns('name').filter('state = 2').call())
    num_services += len(ls.services.columns('description').filter('state = 2').call())


print("0 dashboard services={0};hosts={1} Found Errors on {1} Hosts and {0} Services".format(num_services, num_hosts))
