import kubernetes


class K8sClient:
    def __init__(self, **kwargs):
        kubernetes.config.load_kube_config(config_file=kwargs.get("kubeconfig"))
        config = kubernetes.client.Configuration().get_default_copy()
        self.client = kubernetes.dynamic.DynamicClient(
            kubernetes.client.ApiClient(config)
        )

    def present(self, definition):
        api_version = definition.get("apiVersion")
        kind = definition.get("kind")
        name = definition["metadata"].get("name")
        namespace = definition["metadata"].get("namespace")
        resource = self._get_resource(api_version, kind)
        try:
            instance = resource.get(name=name, namespace=namespace)
            resource.patch(definition, name=name, namespace=namespace)
        except kubernetes.dynamic.exceptions.NotFoundError:
            instance = resource.create(definition, name=name, namespace=namespace)
        return instance.to_dict()

    def absent(self, definition):
        api_version = definition.get("apiVersion")
        kind = definition.get("kind")
        name = definition["metadata"].get("name")
        namespace = definition["metadata"].get("namespace")
        resource = self._get_resource(api_version, kind)
        try:
            resource.delete(name=name, namespace=namespace)
        except kubernetes.dynamic.exceptions.NotFoundError:
            pass
        return {}

    def _get_resource(self, api_version, kind, prefix="api"):
        return self.client.resources.get(
            prefix=prefix, api_version=api_version, kind=kind
        )
