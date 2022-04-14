#!/usr/bin/python


import time

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.gravesm.aws.plugins.module_utils.client import AwsClient
from ansible_collections.gravesm.cloud.plugins.module_utils.resource import run


ARG_SPEC = {
    "resources": {
        "type": "list"
    },
    "state": {
        "type": "str"
    }
}


def main():
    module = AnsibleModule(argument_spec=ARG_SPEC)
    client = AwsClient()
    result = run(module.params.get("resources", []), client, module.params["state"])
    module.exit_json(changed=True, **result)


if __name__ == "__main__":
    main()
