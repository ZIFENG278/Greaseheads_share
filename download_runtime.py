from download import Download
import json


def download_runtime(role_path):
    with open('roles.json', 'r') as f:
        roles_dict = json.load(f)
    # a = roles_dict.items()
    # print(type(a))
    role = Download(role_url=roles_dict.get(role_path), role_path=role_path)
    role.start()

# download_runtime('梦心玥_Candice')


def inspect_update_runtime(role_path):
    with open('roles.json', 'r') as f:
        roles_dict = json.load(f)
    # a = roles_dict.items()
    # print(type(a))
    role = Download(role_url=roles_dict.get(role_path), role_path=role_path)
    role.inspect_update()


def inspect_img_num_runtime(role_path):
    with open('roles.json', 'r') as f:
        roles_dict = json.load(f)
    # a = roles_dict.items()
    # print(type(a))
    role = Download(role_url=roles_dict.get(role_path), role_path=role_path)
    role.inspect_image_num()


# inspect_update_runtime('周九九_JojoBaby')
inspect_img_num_runtime('周九九_JojoBaby')