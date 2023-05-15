from download import Download
import json


def download_runtime(role_path):
    with open('roles.json', 'r') as f:
        roles_dict = json.load(f)

    # a = roles_dict.items()
    # print(type(a))

    role = Download(role_url=roles_dict.get(role_path), role_path=role_path)

    role.start()

download_runtime('朱可儿_Flora')

