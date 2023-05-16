import json
import os


def all_key_value_to_json():
    big_dict = {}
    dist_folders_list = os.listdir('../dist')
    dist_folders_list.remove('anonymous')

    for folder in dist_folders_list:
        #print(folder)
        small_dict = {}
        albums = os.listdir('../dist/' + folder)
        for album in albums:
            small_dict[album[3:]] = album[:3]
        big_dict[folder] = dict(sorted(small_dict.items(), key=lambda item: item[1]))

        # big_dict = sorted(big_dict)

    #print(big_dict)
    # print(big_dict)

    # print(os.path.abspath(os.path.dirname(__file__)))

    # print(dist_folders_list)
    with open('../albums_key_value.json', 'w', encoding='utf8') as f:
        json.dump(big_dict, f, ensure_ascii=False)

    with open('../albums_key_value.json', 'r') as f:
        a = json.load(f)
    # print(a['优优_Yoo'])
    # print(json.dumps(a, indent=4))
    print(json.dumps(a, ensure_ascii=False, indent=4))


def update_singal_role_json():  # TODO implement
    pass

all_key_value_to_json()