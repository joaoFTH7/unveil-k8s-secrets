import json
from types import SimpleNamespace

def objectize(dictionary: dict) -> object:
    return json.loads(
        json.dumps(dictionary),
        object_hook=lambda d: SimpleNamespace(**d)
    )