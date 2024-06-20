import json


def as_json(resp):
    return json.loads(resp.text)
