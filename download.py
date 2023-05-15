import requests
import re
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
from util import mkdir_with_new, get_need_update_num
from concurrent.futures import ThreadPoolExecutor


class Download:
    def __init__(self, role_url, role_path):
        self.role_url = role_url
        self.role_path = role_path
        self.main_url = "https://www.xsnvshen.com"
        self.header = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        }
        self.header_with_referer = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
            "Referer": self.role_url
        }
        self.get_title = re.compile(r'<title>(?P<title>.*?)</title>', re.S)
        self.find_num_picture = re.compile(r'更新.*?<span style.*?共 (?P<num_picture>.*?) 张', re.S)

    def get_pre_data(self, url):  # done
        data = []  # order: jpg_half_link, title, num_picture
        resp = requests.get(url, headers=self.header)
        resp.encoding = 'utf-8'
        # print(resp.text)
        resp_bs = BeautifulSoup(resp.text, "html.parser")
        first_picture_href = resp_bs.find("div", class_="swpt-full-wrap").find("a").get('href')
        # print(first_picture_href)
        full_first_jpg_link = 'https:' + first_picture_href
        # jpg_half_link = get_half_jpg_link.search(full_first_jpg_link).group("half_link")
        jpg_half_link = full_first_jpg_link.rsplit("/", 1)[0] + "/"
        data.append(jpg_half_link)
        title = self.get_title.search(resp.text).group("title")
        # print(title)
        data.append(title)
        picture_num = int(self.find_num_picture.search(resp.text).group("num_picture"))
        # print(picture_num)
        data.append(picture_num)
        # print(data)
        resp.close()
        return data

    def get_all_album_link(self):  # done
        role_main_resp = requests.get(self.role_url, headers=self.header)
        role_main_resp.encoding = 'utf-8'
        # print(ycc_main_resp.text)
        role_main_resp_bs = BeautifulSoup(role_main_resp.text, "html.parser")
        find_main_class = role_main_resp_bs.find("div", class_="star-mod entryAblum")  # 返回string
        # print(find_main_class)
        role_childs = find_main_class.find_all("a")
        # print(ycc_child_name)
        # ycc_folders_list = []
        role_href_list = []
        for role_child in role_childs:
            # title = ycc_child.get('title')
            # print(title)
            # ycc_folders_list.append(title)
            href = role_child.get('href')
            # print(href)
            role_href_list.append(self.main_url + href)

        role_main_resp.close()
        return role_href_list

    async def aiodownload(self, full_link, img_name, folder_name):
        async with aiohttp.ClientSession() as session:
            async with session.get(full_link, headers=self.header_with_referer) as resp:
                jpg_content = await resp.read()
                # print(type(jpg_content), img_name)
                async with aiofiles.open(folder_name + "/" + img_name, 'wb') as f:
                    await f.write(jpg_content)
                    await f.close()
                    #print(folder_name)
            resp.close()
        # print(img_name + " over!")
        await session.close()

    async def get_tasks(self, url, index):
        data = self.get_pre_data(url)
        add_index = str(index).rjust(3, '0')
        folder_name = mkdir_with_new("dist/" + self.role_path + "/" + add_index + data[1])  # 更改路径
        tasks = []
        for jpgs in range(data[2]):
            full_link = data[0] + str(jpgs).rjust(3, '0') + '.jpg'
            # print(full_link)
            img_name = full_link.split("/")[-1]
            tasks.append(self.aiodownload(full_link, img_name, folder_name))

        await asyncio.wait(tasks)
        print(folder_name)

    def down_one_album(self, url, index):
        # print('down_one')
        # signal_album_url = 'https://www.xsnvshen.com/album/39192'
        # get_pre_data(url)
        asyncio.run(self.get_tasks(url, index))

    def start(self):
        access = True
        try:
            all_href = self.get_all_album_link()
            # if self.role_path == "anonymous":  # TODO waring consider sometime url broken
            #     access = True
        except:
            if self.role_path == "anonymous":
                print('\033[93m' + "downloading in " + self.role_path + '\033[0m') # TODO waring consider sometime url broken
            else:
                print('\033[93m' + self.role_path + " url broken. can not access the url. FAIL" + '\033[0m')
                access = False
        if access and self.role_path != "anonymous":
            need_update_num = get_need_update_num(self.role_path, len(all_href))
            with ThreadPoolExecutor(8) as t:  # 更改线程池数量
                for i in range(need_update_num - 1, -1, -1):
                    t.submit(self.down_one_album, url=all_href[i], index=len(all_href) - 1 - i)
                    # time.sleep(60)
                print(self.role_path + "\tupdate: " + str(need_update_num) + "\tTotal: " + str(len(all_href)))
        else:
            self.down_one_album(self.role_url)

