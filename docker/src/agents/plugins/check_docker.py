#! /usr/bin/env python3

"""
Kuhn & Rueß GmbH
Consulting and Development
https://kuhn-ruess.de
"""

# pylint: disable=too-many-branches, too-many-nested-blocks, too-many-locals, too-many-statements
from os import getenv
from os.path import exists, join

import requests

try:
    from docker import APIClient
    from docker.errors import DockerException, APIError
except ImportError:
    print("Python package docker >= 6.1.0 is missing")
    print("Please install it with: <<<pip install docker>>>")


def process_containers(docker_containers, label_whitelist, label_replacements, piggyback):
    """
    Process Containers
    """
    #pprint(docker_containers)
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

    for container_id in docker_containers:
        docker_container = docker_containers[container_id]

        if piggyback and "com.docker.swarm.service.name" in docker_container["Labels"]:
            print(f"<<<<{docker_container['Labels']['com.docker.swarm.service.name']}>>>>")

        print("<<<docker_containers:sep(35)>>>")

        output = []
        output.append(docker_container["Names"][0])

        for item in ["Names", "State", "Status", "Created",
                     "Command", "Image", "ImageID", "SizeRootFs", "SizeRw"]:
            if item in docker_container:
                if "Command" == item:
                    docker_container[item] = docker_container[item].replace("\n", "%%")

                if isinstance(docker_container[item], list):
                    output.append(f"{item}={','.join(docker_container[item])}")
                else:
                    output.append(f"{item}={docker_container[item]}")

        if docker_container["StatsValid"] == "yes":
            # u'cpu_stats': {u'cpu_usage': {u'total_usage': 29103411,}
            #                u'system_cpu_usage': 1120853710000000,}}
            # u'memory_stats': {u'limit': 1040609280,
            #                   u'max_usage': 1540096,
            #                   u'usage': 1404928},

            stats = docker_container["Stats"]

            if docker_container["State"] == "running":
                output.append(f"CPU_usage={stats['cpu_stats']['cpu_usage']['total_usage']}")
                output.append(f"CPU_system_usage={stats['cpu_stats']['system_cpu_usage']}")

                output.append(f"cpu_num={stats['precpu_stats']['online_cpus']}")
                output.append(f"system_ticks={stats['precpu_stats']['system_cpu_usage']}")
                output.append(f"container_ticks={stats['precpu_stats']['cpu_usage']['total_usage']}")

                output.append(f"Memory_used={stats['memory_stats']['usage']}")
                output.append(f"Memory_limit={stats['memory_stats']['limit']}")

        else:
            output.append("Stats=Unable to collect container statistics.")

        if "Labels" in docker_container:
            filtered_labels = {}

            for label_filter in label_whitelist:

                for k,v in docker_container["Labels"].items():
                    if label_filter.endswith("*"):
                        if k.startswith(label_filter[:-1]):
                            filtered_labels[k] = v
                    elif k == label_filter:
                        filtered_labels[k] = v

            if filtered_labels:
                text = "Labels="
                for k, v in filtered_labels.items():
                    text += f"{label_replacements.get(k, k)}?{v}|"
                output.append(text)

        print("#".join(output))
        if piggyback and "com.docker.swarm.service.name" in docker_container["Labels"]:
            print("<<<<>>>>")


def process_images(docker_images):
    """
    Process Docker Images
    """
    # [{u'Containers': -1,
    #   u'Created': 1499283368,
    #   u'Id': u'sha256:2f7f7bce89290f69233351416b0cc8d0c8d4800c825ba92e70de5b1cc048a50a',
    #   u'Labels': {},
    #   u'ParentId': u'',
    #   u'RepoDigests': [u'nginx@sha256:8e2645484fe09122ea8aef7xxx312d47fa51675cbf21d1b4b901a'],
    #   u'RepoTags': [u'nginx:latest'],
    #   u'SharedSize': -1,
    #   u'Size': 107509834,
    #   u'VirtualSize': 107509834},
    # ]

    print("<<<docker_images:sep(35)>>>")

    for docker_image in docker_images:
        output = []
        image_id = docker_image['Id']

        if "RepoTags" in docker_image and \
                docker_image["RepoTags"] is not None and len(docker_image["RepoTags"]) > 0:
            image_name = docker_image["RepoTags"][0]
            diskspace = docker_image["Size"]    # The image uses this space only once

            output.append(image_name)
            output.append(f"ImageID={image_id}")
            output.append(f"Diskspace_used={diskspace}")
            print("#".join(output))


def main():
    """
    Main
    """
    timeout = 30
    piggyback = False
    label_whitelist = []
    label_replacements = {}

    conffile = join(getenv("MK_CONFDIR", "/etc/check_mk"), "check_docker.cfg")
    if exists(conffile):
        with open(conffile, encoding='utf-8') as f:

            current_section = None
            for line in f.readlines():
                line = line.strip()
                if line.startswith("[["):
                    current_section = line
                    continue
                if line.startswith("timeout"):
                    timeout = int(line.split("=")[1])
                    continue
                if line.startswith("piggyback"):
                    if line.split("=")[1] == "True":
                        piggyback = True
                    continue

                if current_section == "[[whitelist]]":
                    label_whitelist.append(line)
                elif current_section == "[[replacements]]":
                    original, replacement = line.split()
                    label_replacements[original] = replacement

    # try to connect to docker service
    try:
        #conn = docker.from_env(timeout=timeout)
        #conn = APIClient(base_url="tcp://127.0.0.1:1234", timeout=timeout, version="auto")
        conn = APIClient(base_url="unix://var/run/docker.sock", timeout=timeout, version="auto")

    except DockerException:
        print("Connection not possible")
        raise

    except Exception:
        print("Unknown error:")
        raise

    # try to get docker info
    try:
        docker_info = conn.info()

        print("<<<docker_info:sep(59)>>>")
        print("service;up")
        print(f"version;{docker_info['ServerVersion']}")
        print(f"images;{docker_info['Images']}")
        print(f"go_routines;{docker_info['NGoroutines']}")
        print(f"file_descriptors;{docker_info['NFd']}")
        print(f"events_listeners;{docker_info['NEventsListener']}")

    except APIError:
        print("<<<docker_info:sep(59)>>>")
        print("service;down")

    containers = {}

    # try to get all containers
    try:
        docker_containers = conn.containers(all=True, size=True)

        for docker_container in docker_containers:
            cont_id = docker_container["Id"]
            containers[cont_id] = docker_container

            # try to get statistics for container
            try:
                #docker_stats = conn.stats(container=cont_id, \
                #                          decode=False, stream=False, one_shot=True)
                docker_stats = conn.stats(container=cont_id, decode=False, stream=False)
                containers[cont_id]["StatsValid"] = "yes"
                containers[cont_id]["Stats"] = docker_stats

            except APIError:
                containers[cont_id]["StatsValid"] = "no"

        process_containers(containers, label_whitelist, label_replacements, piggyback)

    except APIError:
        print("<<<docker_containers:sep(35)>>>")

    # try to get all images
    try:
        images = conn.images(all=True)
        process_images(images)

    except requests.exceptions.ConnectionError:
        print("<<<docker_images:sep(35)>>>")


if __name__ == "__main__":
    main()
