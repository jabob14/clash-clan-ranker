import json
from datetime import datetime, timezone
from config import FILE_PATH

def read_from_file():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_to_file(clan_data):
    with open(FILE_PATH, "w") as f:
        json.dump(clan_data, f, indent=4)
