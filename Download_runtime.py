from downloadClass import Download
import json

with open('roles.json', 'r') as f:
    roles_dict = json.load(f)

# a = roles_dict.items()
# print(type(a))

role = Download(role_url=roles_dict.get('王馨瑶_Yanni'), role_path='王馨瑶_Yanni')

role.start()