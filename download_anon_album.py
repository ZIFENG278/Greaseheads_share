from download import Download

anon = [
    "https://www.xsnvshen.com/album/40963",
    "https://www.xsnvshen.com/album/40967",
]

def download_anon_album(url, path):
    anonymous = Download(url, path)
    anonymous.start()
    # try:
    #     g = p.get_all_album_link()
    # except:
    #     print("ok")
    # g = p.get_pre_data(url)
    # print(g)


download_anon_album("https://www.xsnvshen.com/album/40967", "anonymous")