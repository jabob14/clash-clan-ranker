import json
from datetime import datetime, timezone
from config import FILE_PATH

def read_from_file():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {"error": "File not found"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON"}


def write_to_file(clan_data):
    try:
        with open(FILE_PATH, "w", encoding='utf-8') as f:
            json.dump(clan_data, f, indent=4)
    except Exception as e:
        return {"error": str(e)}
