import json


def read_admin_list(file_dir: str):
    with open(file_dir) as f:
        admin_list = json.load(f)

        return admin_list
