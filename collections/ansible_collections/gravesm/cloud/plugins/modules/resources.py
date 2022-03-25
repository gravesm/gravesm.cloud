#!/usr/bin/python


import time

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.gravesm.cloud.plugins.module_utils.resource import create


ARG_SPEC = {
    "resources": {
        "type": "list"
    }
}


def main():
    module = AnsibleModule(argument_spec=ARG_SPEC)
    resources = module.params.get("resources")
    t0 = time.monotonic()
    result = create(resources)
    t1 = time.monotonic()
    module.exit_json(
        changed=True,
        created=result,
        elapsed=t1-t0,
    )


if __name__ == "__main__":
    main()
