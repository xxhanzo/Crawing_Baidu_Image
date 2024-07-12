# -*- coding:utf8 -*-
import requests
import json
from urllib import parse
import os
import time

class BaiduImageSpider(object):
    def __init__(self):
        self.url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=5179920884740494226&ipn=rj&ct' \
                   '=201326592&is=&fp=result&queryWord={' \
                   '}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word={' \
                   '}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&nojc=&pn={' \
                   '}&rn=30&gsm=1e&1635054081427= '
        self.directory = r"D:\DownloadedImages\{}"  # 修改为你有权限的目录
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30 '
        }

    # 创建存储文件夹
    def create_directory(self, name):
        self.directory = self.directory.format(name)
        # 如果目录不存在则创建
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.directory += r'\{}'

    # 获取图像链接
    def get_image_link(self, url):
        list_image_link = []
        strhtml = requests.get(url, headers=self.header)  # Get方式获取网页数据
        jsonInfo = json.loads(strhtml.text)
        for index in range(30):
            try:
                list_image_link.append(jsonInfo['data'][index]['thumbURL'])
            except (IndexError, KeyError):
                continue
        return list_image_link

    # 下载图片
    def save_image(self, img_link, filename):
        try:
            res = requests.get(img_link, headers=self.header)
            if res.status_code == 404:
                print(f"图片{img_link}下载出错------->")
                return
            with open(filename, "wb") as f:
                f.write(res.content)
                print("存储路径：" + filename)
        except Exception as e:
            print(f"下载图片时出错：{e}")

    # 入口函数
    def run(self):
        searchName = input("查询内容：")
        searchName_parse = parse.quote(searchName)  # 编码
        total_images = int(input("请输入要下载的图片数量："))

        self.create_directory(searchName)

        pic_number = 0  # 图像数量
        json_count = (total_images + 29) // 30  # 计算需要下载的json文件数量
        for index in range(json_count):
            pn = index * 30
            request_url = self.url.format(searchName_parse, searchName_parse, str(pn))
            list_image_link = self.get_image_link(request_url)
            for link in list_image_link:
                if link:
                    pic_number += 1
                    self.save_image(link, self.directory.format(str(pic_number) + '.jpg'))
                    if pic_number >= total_images:
                        print(searchName + "----图像下载完成--------->")
                        return
                    time.sleep(0.2)  # 休眠0.2秒，防止封ip

if __name__ == '__main__':
    spider = BaiduImageSpider()
    spider.run()
