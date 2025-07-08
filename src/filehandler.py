import json
from datetime import datetime, timezone
from config import FILE_PATH

def read_from_file():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_to_file(clan_info, member_info):
    now_utc = datetime.now(timezone.utc)
    iso_string = now_utc.isoformat()
    timestamp_str = iso_string.split('.')[0] + "Z"

    clan_data = {
                "lastUpdated" : timestamp_str,
                "clanInfo" : clan_info,
                "memberInfo" : member_info
            }


    with open(FILE_PATH, "w") as f:
        json.dump(clan_data, f, indent=4)
