import argparse
import os
from random import randint
from time import sleep
import requests

SLEEP_TIME = 30

cookies = {}

headers = {
    'authority': 'afdian.net',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://afdian.net/album/c6ae1166a9f511eab22c52540025c377',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
}


def download_page(data, list: bool, n: int=-1):
    print(data)
    albums = data["list"]
    for album in albums:
        title = album["title"]
        author = album["user"]["name"]
        description = album["content"]
        cover_url = album["audio_thumb"]
        audio_url: str = album["audio"]
        # 是否仅列出
        if list:
            print(title)
        else:
            filename = f"{title}.mp3"
            print(f"正在处理：{title}")
            if audio_url.strip() == "":
                print("本条动态没有音频文件，跳过")
                continue
            cover = None
            try:
                cover = requests.get(cover_url).content
                print(f"封面下载完毕")
            except Exception as e:
                print(f"封面下载失败：{cover_url}")
                print(e)
            try:
                if not os.path.exists(filename):
                    # 没有下载过
                    mp3 = requests.get(audio_url, headers=headers, cookies=cookies).content
                    with open(filename, "wb+") as file:
                        file.write(mp3)
                    print(f"{filename} 下载完成")
                audio: eyed3.core.AudioFile = eyed3.load(filename)
                if audio is None and os.path.exists(filename):
                    # 不知道为什么有些是ISO Media, MP4 Base Media v1，eyed3识别不了
                    print("不支持的音频格式，转码中")
                    # 使用ffmpeg转码
                    if os.system(f"ffmpeg -i \"{filename}\" \"{filename}.mp3\"") == 0:
                        os.remove(filename)
                        os.rename(f"{filename}.mp3", f"{filename}")
                    else:
                        print("转码出错")
                        continue
                audio: eyed3.core.AudioFile = eyed3.load(filename)
                if audio.tag is None:
                    audio.initTag()
                audio.tag.artist = author
                audio.tag.title = title
                audio.tag.album = title
                audio.tag.comments.set(description)
                audio.tag.images.set(3, cover, "image/jpeg")
                audio.tag.save()
                print(f"已完成\n")
            except Exception as e:
                print("下载歌曲失败")
                print(e)
            sleep(SLEEP_TIME + randint(0, 5))


def get_all_albums(album_id: str, list: bool):
    params = {
        'album_id': album_id,
        'lastRank': 0,
        'rankOrder': 'asc',
        'rankField': 'rank',
    }
    while True:
        resp = requests.get('https://afdian.net/api/user/get-album-post', headers=headers, params=params,
                            cookies=cookies).json()
        data = resp["data"]
        download_page(data, list, -1)
        params["lastRank"] += 10
        if list:
            sleep(randint(2, 5))
        else:
            sleep(SLEEP_TIME + randint(0, 5))
        if data["has_more"] == 0:
            # 遍历完毕
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="爱发电下载")
    parser.add_argument("--id", required=True, type=str, help="URL里的id")
    parser.add_argument("--list", action="store_true", help="仅列出，不下载")
    args = parser.parse_args()
    cookies["auth_token"] = '2e1bffb38843f7cc45cc355b918f9110_20230522153958; _gid=GA1.2.1182776355.1686896249; _gat_gtag_UA_116694640_1=1; _ga=GA1.1.1563758643.1684741101; _ga_6STWKR7T9E=GS1.1.1686896249.3.1.1686896256.53.0.0'
    get_all_albums(args.id, args.list)
