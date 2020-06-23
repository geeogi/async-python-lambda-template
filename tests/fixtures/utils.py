import json


def json_fixture(path):
    json_string = open(f"./tests/fixtures/{path}").read()
    json_dict = json.loads(json_string)
    json_string_with_formatting_removed = json.dumps(json_dict)
    return json_string_with_formatting_removed

def string_fixture(path):
    return open(f"./tests/fixtures/{path}").read()
