import concurrent.futures
import re
import time
from graphlib import TopologicalSorter

import yaml


REREG = re.compile(r"resource:(\S+)")


def create_resource(resource):
    time.sleep(3)
    return resource


def create(resources):
    created = []
    graph = {}
    sorter = TopologicalSorter()
    for resource in resources:
        name = resource["name"]
        graph[name] = resource
        sorter.add(name, *REREG.findall(yaml.dump(resource)))

    sorter.prepare()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        while sorter.is_active():
            futures = []
            for node in sorter.get_ready():
                 futures.append(executor.submit(create_resource, graph[node]))
            done, _ = concurrent.futures.wait(futures)
            for future in done:
                result = future.result()
                created.append(result)
                sorter.done(result["name"])
    return created
