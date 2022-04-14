import copy

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        result = super().run(tmp, task_vars)
        module_args = copy.deepcopy(self._task.args)
        module_args["resources"] = task_vars.get(self._task.name, [])
        return self._execute_module(module_name=self._task.action, module_args=module_args, task_vars=task_vars)