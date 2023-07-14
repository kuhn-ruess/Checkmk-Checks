#! /usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#import docker

# "pip install docker" is your friend. Please use version 2.5.1 or newer
from docker import APIClient
import pprint
import requests
import os

api_timeout = 30	# 30s is the default. Adjust to your needs!

def process_containers(docker_containers, label_whitelist):

    print("<<<docker_containers:sep(35)>>>")

    #pprint.pprint(docker_containers)
    # [{u'Command': u"nginx -g 'daemon off;'",
    #   u'Created': 1499762426,
    #   u'HostConfig': {u'NetworkMode': u'default'},
    #   u'Image': u'nginx',
    #   u'Names': [u'/nginx'],
    #   u'SizeRootFs': 107607244,
    #   u'SizeRw': 97410,
    #   u'State': u'running',
    #   u'Status': u'Up 2 hours'},
    # ]

    for id in docker_containers:
        #pprint.pprint(docker_container)
        line = []
        docker_container = docker_containers[id]
        line.append(docker_container['Names'][0])
        if 'Names' in docker_container: 
            line.append('Names=%s' % ','.join(docker_container['Names']))
        if 'State' in docker_container: 
            line.append('State=%s' % docker_container['State'])
        if 'Status' in docker_container: 
            line.append('Status=%s' % docker_container['Status'])
        if 'Created' in docker_container: 
            line.append('Created=%s' % docker_container['Created'])
        if 'Command' in docker_container: 
            line.append('Command=%s' % docker_container['Command'])
        if 'Image' in docker_container: 
            line.append('Image=%s' % docker_container['Image'])
        if 'ImageID' in docker_container:
            line.append('ImageID=%s' % docker_container['ImageID'])
        if 'SizeRootFs' in docker_container:
            line.append('SizeRootFs=%s' % docker_container['SizeRootFs'])
        if 'SizeRw' in docker_container:
            line.append('SizeRw=%s' % docker_container['SizeRw'])

        if docker_container['StatsValid'] == 'yes':
            stats = docker_container['Stats']

            # u'cpu_stats': {u'cpu_usage': {u'total_usage': 29103411,}
            #                u'system_cpu_usage': 1120853710000000,}}
            # u'memory_stats': {u'limit': 1040609280,
            #                   u'max_usage': 1540096,
            #                   u'usage': 1404928},

            if docker_container['State'] == 'running':
                line.append('CPU_usage=%f' % stats['cpu_stats']['cpu_usage']['total_usage'])
                line.append('CPU_system_usage=%f' % stats['cpu_stats']['system_cpu_usage'])

                line.append('Memory_used=%d' % stats['memory_stats']['usage'])
                line.append('Memory_limit=%d' % stats['memory_stats']['limit'])
        elif docker_container['StatsValid'] == 'timeout':
            line.append('Stats=Unable to collect container statistics. Timeout!')
        else:
            line.append('Stats=Unable to collect container statistics.')

        if 'Labels' in docker_container:
            filtered_labels = {}
            for label_filter in label_whitelist:
                for k,v in docker_container['Labels'].items():
                    if label_filter.endswith('*'):
                        if k.startswith(label_filter[:-1]):
                            filtered_labels[k] = v
                    elif k == label_filter:
                        filtered_labels[k] = v
            if filtered_labels:
                line.append('Labels='+"|".join("%s:%s" % (k, v) for k, v in filtered_labels.items()))

        print("#".join(line))

    return


def process_images(docker_images, docker_containers):

    print("<<<docker_images:sep(35)>>>")

    # [{u'Containers': -1,
    #   u'Created': 1499283368,
    #   u'Id': u'sha256:2f7f7bce89290f69233351416b0cc8d0c8d4800c825ba92e70de5b1cc048a50a',
    #   u'Labels': {},
    #   u'ParentId': u'',
    #   u'RepoDigests': [u'nginx@sha256:8e2645484fe09122ea8aef7a186658082a860312d47fa51675cbf21d1b4b901a'],
    #   u'RepoTags': [u'nginx:latest'],
    #   u'SharedSize': -1,
    #   u'Size': 107509834,
    #   u'VirtualSize': 107509834},
    # ]

    for docker_image in docker_images:
        line = []
        
        image_id = docker_image['Id']
        if 'RepoTags' in docker_image and docker_image['RepoTags'] is not None and len(docker_image['RepoTags']) > 0:
            image_name = docker_image['RepoTags'][0]
            diskspace = docker_image['Size']    # The image uses this space only once
    
            line.append(image_name)
            line.append("ImageID=" + image_id)
            line.append("Diskspace_used=%d" % diskspace)
            print("#".join(line))

    return


# If the nagios plugin aborts with an uncaught exception or timeout, it exits with 
# an unknown exit code and prints a traceback in a format acceptable by Nagios.

def main():
    label_whitelist = []
    conffile = os.path.join(os.getenv("MK_CONFDIR", "/etc/check_mk"), "check_docker.cfg")
    if os.path.exists(conffile):
        with open(conffile) as f:
            for line in f.readlines():
                label_whitelist.append(line.strip())
    containers = {}

    #conn = docker.from_env(timeout=10)
    conn = APIClient(base_url='unix://var/run/docker.sock', timeout=api_timeout, version='auto')

    try:
        docker_info = conn.info()

        # try to connect the docker service, and catch an exception if we can't.
        print("<<<docker_info:sep(59)>>>")
        print('service;up')
        print('images;%s' % docker_info['Images'])
        print('go_routines;%s' % docker_info['NGoroutines'])
        print('file_descriptors;%s' % docker_info['NFd'])
        print('events_listeners;%s' % docker_info['NEventsListener'])

        docker_containers = conn.containers(all=1, size=1)

        for docker_container in docker_containers:
            cont_id = docker_container['Id']
            containers[cont_id] = docker_container
            try:
                docker_stats = conn.stats(docker_container['Id'], decode=False, stream=False, one_shot=True)
                containers[cont_id]['StatsValid'] = 'yes'
                containers[cont_id]['Stats'] = docker_stats
            except:
                containers[cont_id]['StatsValid'] = 'timeout'
                pass

        images = conn.images(all=1)

        process_containers(containers, label_whitelist)
        process_images(images, containers)

    except requests.exceptions.ConnectionError as objectname:
        print("<<<docker_info:sep(59)>>>")
        print('service;down')
        print("<<<docker_containers:sep(35)>>>")
        print("<<<docker_images:sep(35)>>>")
    except:
        print("Unexpected error:")
        raise


if __name__ == '__main__':
    main()
