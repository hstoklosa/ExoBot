import json

def read_json_file(path_to_file):
    with open(path_to_file) as p:
        return json.load(p)
