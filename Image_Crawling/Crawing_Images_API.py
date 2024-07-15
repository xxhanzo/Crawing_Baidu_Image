# -*- coding:utf8 -*-
import requests
import json
from urllib import parse
import time
from flask import Flask, request, jsonify
from fake_useragent import UserAgent
from collections import OrderedDict

app = Flask(__name__)

class BaiduImageSpider(object):
    def __init__(self):
        self.url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=5179920884740494226&ipn=rj&ct' \
                   '=201326592&is=&fp=result&queryWord={' \
                   '}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word={' \
                   '}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&nojc=&pn={' \
                   '}&rn=30&gsm=1e&1635054081427= '
        self.ua = UserAgent()

    # 获取图像链接
    def get_image_link(self, url):
        list_image_link = []
        headers = {'User-Agent': self.ua.random}
        strhtml = requests.get(url, headers=headers)  # Get方式获取网页数据
        jsonInfo = json.loads(strhtml.text)
        for index in range(30):
            try:
                list_image_link.append(jsonInfo['data'][index]['thumbURL'])
            except (IndexError, KeyError):
                continue
        return list_image_link

    # 获取图片链接
    def get_images(self, search_name, total_images):
        search_name_parse = parse.quote(search_name)  # 编码
        image_links = OrderedDict()
        pic_number = 0  # 图像数量
        json_count = (total_images + 29) // 30  # 计算需要下载的json文件数量
        for index in range(json_count):
            pn = index * 30
            request_url = self.url.format(search_name_parse, search_name_parse, str(pn))
            list_image_link = self.get_image_link(request_url)
            for link in list_image_link:
                if link:
                    pic_number += 1
                    image_links[f"Image_{pic_number}"] = link
                    if pic_number >= total_images:
                        return image_links
                    time.sleep(0.2)  # 休眠0.2秒，防止封ip
        return image_links

@app.route('/crawl_images', methods=['POST'])
def crawl_images():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input, no JSON provided'}), 400

    query = data.get('query')
    num_images = data.get('num_images')
    if not query or not num_images:
        return jsonify({'error': 'Invalid input, query and num_images are required'}), 400

    spider = BaiduImageSpider()
    image_links = spider.get_images(query, num_images)

    # 构建所需的响应格式
    response_list = []
    for key, value in image_links.items():
        response_list.append({
            "Image_name": key,
            "Image_url": value
        })

    return jsonify(response_list)

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=8000, debug=True)
