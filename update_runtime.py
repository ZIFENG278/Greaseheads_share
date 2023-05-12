from download import Download
import json
from concurrent.futures import ThreadPoolExecutor

with open('roles.json', 'r') as f:
    roles_dict = json.load(f)

# a = roles_dict.items()
# print(type(a))
if __name__ == '__main__':
    print("++++++++++update start++++++++++")
    with ThreadPoolExecutor(4) as t:
        for k, v in roles_dict.items():
            # print(k, v)
            role = Download(role_url=v, role_path=k)
            t.submit(role.start)

#     role = Download(role_url=roles_dict.get('王馨瑶_Yanni'), role_path='王馨瑶_Yanni')
#
# role.start()