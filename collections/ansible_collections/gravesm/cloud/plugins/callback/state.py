import json

from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_NAME = "gravesm.cloud.state"
    CALLBACK_TYPE = "aggregate"

    def v2_runner_on_ok(self, result):
        try:
            with open("state.json") as fp:
                state = json.load(fp)
        except:
            state = {}
        resource = "{}/{}".format(result._task_fields["action"], result.task_name)
        state[resource] = result._result.get("resources", {})
        with open("state.json", "w") as fp:
            json.dump(state, fp, indent=True)
