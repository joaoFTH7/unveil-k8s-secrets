from kubernetes import client
from typing import Dict, List


#verify kwargs
class UnveilSecrets:
    def __init__(self, workload_type: str):
        self.workload_type = workload_type


    #fix
    # def get_pod_spec(self):
    #     k8s_client = client.CoreV1Api()

    #     choosed_pod = k8s_client.read_namespaced_pod(name=self.pod_name, namespace=self.namespace_name)

    #     return choosed_pod


    # def get_secrets_from_pod(self):
    #     pod_spec = self.get_pod_spec()

    #     pod_secrets = {
    #         "App Name": pod_spec.metadata.labels.get("alias"),
    #         "UUID": pod_spec.metadata.labels.get("app"),
    #         "Namespace": pod_spec.metadata.labels.get("namespace"),
    #         "App Type": pod_spec.metadata.labels.get("type"),
    #         "Secrets": pod_spec.spec.containers[1].env if self.has_side_car == "yes" else pod_spec.spec.containers[0].env
    #     }

    #     return pod_secrets


    def get_secrets_from_deployment(self) -> Dict[str, any]:
        _, deploy_spec = self.get_deployments()

        deploy_secrets = {
            "App Name": deploy_spec.metadata.labels.get("alias"),
            "UUID": deploy_spec.metadata.name,
            "Namespace": deploy_spec.metadata.labels.get("namespace"),
            "App Type": deploy_spec.metadata.labels.get("type"),
            "Secrets": deploy_spec.spec.template.spec.containers[0].env
        }

        return deploy_secrets


    def get_secrets_from_cronjob(self) -> Dict[str, any]:
        _, cronjob_spec = self.get_cronjobs()
        
        cronjob_secrets = {
            "App Name": cronjob_spec.metadata.labels.get("alias"),
            "UUID": cronjob_spec.metadata.name,
            "Namespace": cronjob_spec.metadata.labels.get("namespace"),
            "App Type": cronjob_spec.metadata.labels.get("type"),
            "Secrets": cronjob_spec.spec.job_template.spec.template.spec.containers[0].env
        }

        return cronjob_secrets


    def exporting_to_textfile(self, workload: any) -> None:
        with open(f"{workload.get('App Name', 'someapp')}-secrets.txt", "w") as file:
            for key, value in workload.items():
                if "Secrets" not in key:
                    file.writelines(f"{key}: {value}\n")
                else:
                    for secret in value:
                        file.writelines(f"{secret.name}: {secret.value}\n")
        
        print(f"Generated \033[1m{workload.get('App Name', 'someapp')}-secrets.txt")
    

    def get_namespaces(self) -> any:
        k8s_client = client.CoreV1Api()

        namespaces = k8s_client.list_namespace()

        return namespaces
    

    def get_deployments(self) -> any:
        namespaces, choosed_namespaced = self.ordering_kubernetes_resources(self.get_namespaces(), "namespace")
        k8s_client = client.AppsV1Api()

        deployments = k8s_client.list_namespaced_deployment(namespace=namespaces[choosed_namespaced])

        deploys_list, choosed_deploy = self.ordering_kubernetes_resources(deployments, "deployments")
        choosed_deployment = k8s_client.read_namespaced_deployment(namespace=namespaces[choosed_namespaced], name=deploys_list[choosed_deploy])

        return deployments, choosed_deployment


    def get_cronjobs(self) -> any:
        namespaces, choosed_namespaced = self.ordering_kubernetes_resources(self.get_namespaces(), "namespace")
        k8s_client = client.BatchV1Api()

        cronjobs = k8s_client.list_namespaced_cron_job(namespace=namespaces[choosed_namespaced])

        cronjobs_list, choosed_cron = self.ordering_kubernetes_resources(cronjobs, "cronjobs")
        choosed_cronjob = k8s_client.read_namespaced_cron_job(namespace=namespaces[choosed_namespaced], name=cronjobs_list[choosed_cron])

        return cronjobs, choosed_cronjob


    def ordering_kubernetes_resources(self, resource: any, resource_type: str) -> tuple[List, int]:
        resource_alias_list = [
            f'Name: {resources.metadata.labels.get("alias")} UUID: {resources.metadata.name}' 
            if resources.metadata.labels.get("alias") else resources.metadata.name 
            for resources in resource.items
        ]

        resource_alias_list.sort()

        resource_name_list = []
        for index, resources in enumerate(resource_alias_list):
            print(f"{index}-{resources}")
            
            pos = resources.find("UUID") if resources.find("UUID") > 0 else 0
            uuid = resources[pos+6:] if pos > 0 else resources
            resource_name_list.append(uuid)
            

        choosed_resource = int(input(f"Choose a {resource_type} according to the number..: "))

        return resource_name_list, choosed_resource
