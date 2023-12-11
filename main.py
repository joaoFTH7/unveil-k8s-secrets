from choose import loading_contexts
from unveil_secrets import UnveilSecrets

def main():
    print("Unveil Kubernetes Secrets")
    
    loading_contexts()


    workloads = ["deployment", "cronjob", "pod"]
    for index, workload in enumerate(workloads):
        print(f"{index}-{workload}")
    
    workload_type = int(input("Choose a workload type according to the number..: "))
    
    instance = UnveilSecrets(workload_type=workloads[workload_type])

    if workloads[workload_type] == "deployment":
        secrets = instance.get_secrets_from_deployment()
        instance.exporting_to_textfile(secrets)
    elif workloads[workload_type] == "cronjob":
        secrets = instance.get_secrets_from_cronjob()
        instance.exporting_to_textfile(secrets)
    elif workloads[workload_type] == "pod":
        raise NotImplementedError
    else:
        raise IndexError


if __name__ == "__main__":
    main()
