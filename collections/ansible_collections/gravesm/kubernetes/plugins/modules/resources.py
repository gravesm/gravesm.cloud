#!/usr/bin/python


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.gravesm.cloud.plugins.module_utils.resource import run
from ansible_collections.gravesm.kubernetes.plugins.module_utils.client import K8sClient


ARG_SPEC = {
    "resources": {"type": "list"},
    "state": {"type": "str"},
    "current_state": {"type": "dict"},
    "connection": {"type": "dict"},
}


def main():
    module = AnsibleModule(argument_spec=ARG_SPEC)
    client = K8sClient(**module.params.get("connection"))
    result = run(
        module.params.get("resources", []),
        module.params.get("current_state", {}),
        client,
        module.params["state"],
    )
    module.exit_json(changed=True, resources=result)


if __name__ == "__main__":
    main()
