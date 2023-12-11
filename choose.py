from typing import Dict, List
from kubernetes import config

from helpers.objectize import objectize


def listing_contexts() -> List:
    context_list, _ = objectize(config.list_kube_config_contexts())

    n = 0
    list_context = []

    for settings in context_list:
        contexts = settings.context.cluster
        list_context.append(contexts)

        print(f"{n}-{contexts}")
        
        n = n + 1
    
    return list_context


def loading_contexts(choosed_context: list = []) -> List:
    list_all_contexts = listing_contexts()

    choosed_context = int(input("Choose one context to load according to the number.: "))

    _ = config.load_kube_config(context=list_all_contexts[choosed_context])

    return list_all_contexts[choosed_context]
