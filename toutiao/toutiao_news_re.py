#!/usr/bin/python3
#!coding=utf-8

import requests
import re
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pymysql
import traceback
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  ###禁止提醒SSL警告


def start():
    news_type = '{"news_type":[{"type":"selected","name":"推荐","id":"BA8J7DG9wangning"}]}'

    news = json.loads(news_type)

    for data in news['news_type']:
        url = 'https://www.toutiao.com/ch/%s/' % data['type']
        print(url)
        request_data(url, data['name'], data['id'])


def request_data(url=None, name=None, id=None):  ####APP模式
    driver = web_driver()
    channel = re.search('ch/(.*?)/', url).group(1)
    s = requests.session()
    headers = {
        'Accept': 'image/webp,image/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36',
        'Accept-Language': 'zh-cn'
     }
    s.headers.update(headers)

    t2 = int(time.time()) - 2000

    for i in range(20):  ###爬取页数
        time.sleep(3)
        t = int(time.time())
        params = {
            'category': channel,  ###频道名
            'refer': '1',  ###???，固定值1
            'count': '20',  ####返回数量，默认为20
            'min_behot_time': t2,  ####上次请求时间的时间戳，例:1491981025
            'last_refresh_sub_entrance_interval': t - 10,  #####本次请求时间的时间戳，例:1491981165
            'loc_time': int(t / 1000) * 1000,  ###本地时间
            'latitude': '',  ###经度
            'longitude': '',  ###纬度
            'city': '',  ###当前城市
            'iid': '1234876543',  ###某个唯一 id，长度为10
            'device_id': '42433242851',  ###设备id，长度为11
            'abflag': '3',
            'ssmix': 'a',
            'language': 'zh',
            'openudid': '1b8d5bf69dc4a561',  ####某个唯一id，长度为16

        }

        url = 'http://is.snssdk.com/api/news/feed/v51/'
        app = s.get(url=url, params=params, verify=False).json()
        print(app)
        t2 = t - 10
        total_number = app['total_number']

        for j in range(0, total_number):

            content = json.loads(app['data'][j]['content'])

            if ('video_detail_info' in content):
                continue

            try:
                images = content['image_list']
                imgsrc = ''
                for img in images:
                    imgsrc = imgsrc + img['url'][:-5] + ','
                content['imgsrc'] = imgsrc
            except KeyError:
                content['imgsrc'] = ''

            try:
                url = content['display_url']

                # driver.get(url)
                # source = driver.page_source
                #
                # soup = BeautifulSoup(source, "html.parser")
                # content['content'] = str(soup.find_all(class_='article-content')[0])
            except:
                content['content'] = ''

            content['news_type'] = name
            content['news_id'] = id
            content['ptime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(content['publish_time']))
            content['editor'] = content['user_info']['name']

            # if content['content'] != '' and content['content'] is not None:
            #     on_result(content)

    driver.quit()
    s.close()


def web_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36')
    driver = webdriver.Firefox(executable_path='D:\geckodriver\geckodriver.exe', options=options)
    # driver = webdriver.Firefox(options=options)

    return driver

def on_result(result=None):

    try:
        conn = pymysql.connect(host="47.101.146.57", port=2018, user="root", password="Liuku!!!111",
                                    db="dm_report", charset='utf8')
        conn.autocommit = True

        cursor = conn.cursor()

        row = cursor.execute('''select id from toutiao_news_latest where url='{}';'''.format(result['display_url']))

        if row == 0:

            sql = '''insert into toutiao_news(title,news_time,url,from_source,author,news_type,digest,contents,commentCount,image_url,check_status,tag,news_id) values ({}','{}','{}','{}','{}','{}','{}', '{}','{}','{}','{}','{}','{}');'''.format(
                result['title'].replace(chr(39), "\\'"), result['ptime'], result['display_url'], result['source'],
                result['editor'], result['news_type'], result['abstract'].replace(chr(39), "\\'"), result['content'].replace(chr(39), "\\'"),
                result['comment_count'], result['imgsrc'], '0', result['news_id'],result['tag_id'])

            cursor.execute(sql)
            conn.commit()
            print("数据保存成功")

    except Exception as e:
        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    while True:
        start()

