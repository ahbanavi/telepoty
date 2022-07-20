import json

DATA_FILE_PATH = 'data.json'

def read_data():
    try:
        with open(DATA_FILE_PATH, "r") as json_file:
            return json.load(json_file)
    except:
        return {"items": [], "min_id": 0}


def write_data(data):
    with open(DATA_FILE_PATH, "w") as outfile:
        json.dump(data, outfile, indent=4)