# 	mm图片爬虫工具（油头党专用）

> 爬虫实战
>
> 本次针对非客户端渲染的无加密的图片网站下手，因为无聊发现一个更新速度快，图册完善且非常适合爬取的第三方图片网[点击跳转](https://www.xsnvshen.com)，测试时在国外测试的，不清楚国内是否被墙，看具体情况科学上网。
>
> Linux/mac用户安装所需库后添加文件夹后修改保存路径后可直接运行
>
> windows用户需修改保存路径的反斜杠



## Linux/Mac Usage

> 推荐使用conda环境 ***python>=3.7***

```
git clone https://github.com/ZIFENG278/Greaseheads_share.git
```

需要抓取master分支(直接clone在mian支无内容的)

安装所需环境

```
pip3 install -r requirements.txt
```

**在代码同目录先新建一个你喜欢的角色名的文件夹，并在get_tasks函数处修改路径**

![picture](/home/zifeng/Pictures/Screenshots/zz1.png)

**挑选你喜欢的角色复制url到url_ycc_main处 否则默认推荐角色**

![picture](/home/zifeng/Pictures/Screenshots/zz2.png)

```
python3 auto_download_xiecheng.py
```

**mac M1芯片16线程测试时初段直接显示open too much file自动终止，需要减少线程的数量**

**实测ubuntu开16线程偶尔也有部分段open too much file, 建议12或8，看cpu性能选择合适线程**

**默认线程池为8**





## 开发思路

> python爬虫

1. 利用requests对人物的主页进行访问，获取源码后放进BeautifulSoup里，通过标签查找找出主页所有图册的href

   ```python
   def get_all_album_link(url):
       ycc_main_resp = requests.get(url, headers=header)
       ycc_main_resp.encoding = 'utf-8'
       # print(ycc_main_resp.text)
       ycc_main_resp_bs = BeautifulSoup(ycc_main_resp.text, "html.parser")
       find_main_class = ycc_main_resp_bs.find("div", class_="star-mod entryAblum")  # 返回string
       # print(find_main_class)
       ycc_childs = find_main_class.find_all("a")
       # print(ycc_child_name)
       # ycc_folders_list = []
       ycc_href_list = []
       for ycc_child in ycc_childs:
           # title = ycc_child.get('title')
           # print(title)
           # ycc_folders_list.append(title)
           href = ycc_child.get('href')
           # print(href)
           ycc_href_list.append(url_2 + href)
   
       ycc_main_resp.close()
       return ycc_href_list
   ```

   

2. 通过多线程对每个href先进行同步线程访问获取网页源码, 首先利用BeautifulSoup与正则表达式获取相册的名字以作文件夹名称与第一张jpg的url和单个图册的图片数,因为网页源码实质提供了所有低清预览，但有第一张高清预览图jpg的url, 需要简单拼接一下得到完整的单个高清图url, 所以需要提取前半段的url

   ```python
   def get_pre_data(url):
       data = []  # order: jpg_half_link, title, num_picture
       resp = requests.get(url, headers=header)
       resp.encoding = 'utf-8'
       # print(resp.text)
       resp_bs = BeautifulSoup(resp.text, "html.parser")
       first_picture_href = resp_bs.find("div", class_="swpt-full-wrap").find("a").get('href')
       # print(first_picture_href)
       full_first_jpg_link = 'https:' + first_picture_href
       jpg_half_link = get_half_jpg_link.search(full_first_jpg_link).group("half_link")
       data.append(jpg_half_link)
       title = get_title.search(resp.text).group("title")
       # print(title)
       data.append(title)
       picture_num = int(find_num_picture.search(resp.text).group("num_picture"))
       # print(picture_num)
       data.append(picture_num)
       print(data)
       resp.close()
       return data
   ```



3. 得到所有预处理数据后，利用协程进行异步访问与异步写入，用到asyncio，aiohttp ，aiofiles 三个库，因为网站有时候会存在相同名称的图集，所以遇到相同名称的后面加上new防止覆盖，宁可多下也不愿意错过

   **window用户需要修改一下路径，改成反斜杠，mkdir函数不清楚window用户是否能跑，可能要稍微改改**

   ```python
   def mkdir(path):
       while True:
           folder = os.path.exists(path)
           if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
               os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
               print("---  new folder...  ---")
               # print("---  OK  ---")
               break
           else:
               print("---  There already have this folder!  ---")
               path = path + "new"
               continue
   
       return path
   
   
   async def aiodownload(full_link, img_name, folder_name):
       async with aiohttp.ClientSession() as session:
           async with session.get(full_link, headers=header2) as resp:
               jpg_content = await resp.read()
               # print(type(jpg_content), img_name)
               async with aiofiles.open(folder_name + "/" + img_name, 'wb') as f:
                   await f.write(jpg_content)
                   # await f.close()
       print(img_name + " over!")
   
   
   async def get_tasks(url):
       data = get_pre_data(url)
       folder_name = mkdir("pa_qilijia_project/" + data[1])  # 不同系统需要进行路径修改反斜杠
       tasks = []
       for jpgs in range(data[2]):
           full_link = data[0] + str(jpgs).rjust(3, '0') + '.jpg'
           # print(full_link)
           img_name = full_link.split("/")[-1]
           tasks.append(aiodownload(full_link, img_name, folder_name))
   
       await asyncio.wait(tasks)
   
   
   def down_one_album(url):
       # signal_album_url = 'https://www.xsnvshen.com/album/39192'
       # get_pre_data(url)
       asyncio.run(get_tasks(url))
   ```



## 完整代码

```python
import requests
import re
import asyncio
import aiohttp
import aiofiles
import os
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
# import time

# 同步  1.打开图包页，获得所有jpg的子链接
# 异步下载到文件中

url_ycc_main = "https://www.xsnvshen.com/girl/18220"  # 要下载不同角色，替换这里的角色主页url
url_2 = "https://www.xsnvshen.com"

header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

header2 = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "Referer": url_ycc_main

}

get_title = re.compile(r'<title>(?P<title>.*?)</title>', re.S)

find_num_picture = re.compile(r'更新.*?<span style.*?共 (?P<num_picture>.*?) 张', re.S)

get_half_jpg_link = re.compile(r'(?P<half_link>.*?)000.jpg')


def mkdir(path):
    while True:
        folder = os.path.exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
            print("---  new folder...  ---")
            # print("---  OK  ---")
            break
        else:
            print("---  There already have this folder!  ---")
            path = path + "new"
            continue

    return path


def get_pre_data(url):
    data = []  # order: jpg_half_link, title, num_picture
    resp = requests.get(url, headers=header)
    resp.encoding = 'utf-8'
    # print(resp.text)
    resp_bs = BeautifulSoup(resp.text, "html.parser")
    first_picture_href = resp_bs.find("div", class_="swpt-full-wrap").find("a").get('href')
    # print(first_picture_href)
    full_first_jpg_link = 'https:' + first_picture_href
    jpg_half_link = get_half_jpg_link.search(full_first_jpg_link).group("half_link")
    data.append(jpg_half_link)
    title = get_title.search(resp.text).group("title")
    # print(title)
    data.append(title)
    picture_num = int(find_num_picture.search(resp.text).group("num_picture"))
    # print(picture_num)
    data.append(picture_num)
    print(data)
    resp.close()
    return data


async def aiodownload(full_link, img_name, folder_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(full_link, headers=header2) as resp:
            jpg_content = await resp.read()
            # print(type(jpg_content), img_name)
            async with aiofiles.open(folder_name + "/" + img_name, 'wb') as f:
                await f.write(jpg_content)
                # await f.close()
    print(img_name + " over!")


async def get_tasks(url):
    data = get_pre_data(url)
    folder_name = mkdir("pa_qilijia_project/" + data[1])  # 更不同角色的改路径名称
    tasks = []
    for jpgs in range(data[2]):
        full_link = data[0] + str(jpgs).rjust(3, '0') + '.jpg'
        # print(full_link)
        img_name = full_link.split("/")[-1]
        tasks.append(aiodownload(full_link, img_name, folder_name))

    await asyncio.wait(tasks)


def down_one_album(url):
    # signal_album_url = 'https://www.xsnvshen.com/album/39192'
    # get_pre_data(url)
    asyncio.run(get_tasks(url))


def get_all_album_link(url):
    ycc_main_resp = requests.get(url, headers=header)
    ycc_main_resp.encoding = 'utf-8'
    # print(ycc_main_resp.text)
    ycc_main_resp_bs = BeautifulSoup(ycc_main_resp.text, "html.parser")
    find_main_class = ycc_main_resp_bs.find("div", class_="star-mod entryAblum")  # 返回string
    # print(find_main_class)
    ycc_childs = find_main_class.find_all("a")
    # print(ycc_child_name)
    # ycc_folders_list = []
    ycc_href_list = []
    for ycc_child in ycc_childs:
        # title = ycc_child.get('title')
        # print(title)
        # ycc_folders_list.append(title)
        href = ycc_child.get('href')
        # print(href)
        ycc_href_list.append(url_2 + href)

    ycc_main_resp.close()
    return ycc_href_list


if __name__ == '__main__':
    all_href = get_all_album_link(url_ycc_main)
    with ThreadPoolExecutor(16) as t:
        for i in range(len(all_href) - 1, -1, -1):
            t.submit(down_one_album, url=all_href[i])
            # time.sleep(60)


```

