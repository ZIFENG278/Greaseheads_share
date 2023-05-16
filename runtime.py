from download import Download
import json
from concurrent.futures import ThreadPoolExecutor


def update_runtime():
    with open('roles.json', 'r') as f:
        roles_dict = json.load(f)
    # a = roles_dict.items()
    # print(type(a))
    print("++++++++++update start++++++++++")
    with ThreadPoolExecutor(8) as t:
        for k, v in roles_dict.items():
            # print(k, v)
            role = Download(role_url=v, role_path=k)
            t.submit(role.start)

    #     role = Download(role_url=roles_dict.get('王馨瑶_Yanni'), role_path='王馨瑶_Yanni')
    #
    # role.start()


def download_runtime(role_path):
    with open('roles.json', 'r') as f:
        roles_dict = json.load(f)

    # a = roles_dict.items()
    # print(type(a))
    role = Download(role_url=roles_dict.get(role_path), role_path=role_path)
    role.start()


def inspect_update_runtime():
    with open('roles.json', 'r') as f:
        roles_dict = json.load(f)
    print("++++++++++update inspect start++++++++++")
    with ThreadPoolExecutor(8) as t:
        for k, v in roles_dict.items():
            # print(k, v)
            role = Download(role_url=v, role_path=k)
            t.submit(role.inspect_update)
    # a = roles_dict.items()
    # print(type(a))
    # role = Download(role_url=roles_dict.get(role_path), role_path=role_path)
    # role.inspect_update()


def inspect_img_num_runtime(role_path):
    with open('roles.json', 'r') as f:
        roles_dict = json.load(f)
    # a = roles_dict.items()
    # print(type(a))
    role = Download(role_url=roles_dict.get(role_path), role_path=role_path)
    role.inspect_image_num()