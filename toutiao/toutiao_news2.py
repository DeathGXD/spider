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

def ttapi(url):  ####APP模式
    channel = re.search('ch/(.*?)/', url).group(1)
    # print(channel)
    s = requests.session()
    headers = {
        'Accept': 'image/webp,image/*;q=0.8',
        'User-Agent': 'News/6.9.8.36 CFNetwork/975.0.3 Darwin/18.2.0',
        'Accept-Language': 'zh-cn'
    }
    s.headers.update(headers)

    t2 = int(time.time()) - 500

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

            try:
                abstract = content['abstract']  ##简报

            except:
                abstract = ''
            try:
                title = content['title']  ##标题
                # result['title'] = title
            except:
                title = ''

            try:
                comment_count = content['comment_count']  ##评论数
                # result['commentCount'] = comment_count
            except:
                comment_count = ''

            try:
                images = content['image_list']
                imgsrc = ''
                for img in images:
                    imgsrc = imgsrc + img['url'] + ','
                content['imgsrc'] = imgsrc
            except KeyError:
                content['imgsrc'] = ''

            try:
                publish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(content['publish_time']))  ##推送时间
                # result['news_time'] = publish_time
            except:
                publish_time = ''

            try:
                source = content['source']  ###新闻来源
                # result['source'] = source
            except:
                source = ''
            try:
                user_info_name = content['user_info']['name']  ##作者名称
                # result['author'] = user_info_name
            except:
                user_info_name = ''

            try:
                url = content['display_url']

                # options = Options()
                # options.add_argument('-headless')
                # driver = webdriver.Firefox(executable_path='D:\geckodriver\geckodriver.exe', options=options)
                # driver.get(url)
                # source = driver.page_source
                #
                # soup = BeautifulSoup(source, "html.parser")
            except:
                content['content'] = ''

            try:
                tag = content['tag']
            except:
                tag = ''

            try:
                news_id = content['tag_id']
            except:
                news_id = ''

            content['channel'] = channel
            # print(content['display_url'])
            # print(content['content'])
            # print(content['imgsrc'])
            print(content['tag'])
            print(content['tag_id'])
            print(content['user_info']['name'])

            # if content['content'] != '':
            #     on_result(content)

    s.close()


def on_result(result=None):
    print(result)
    try:
        conn = pymysql.connect(host="47.101.146.57", port=2018, user="root", password="Liuku!!!111",
                                    db="dm_report", charset='utf8')
        conn.autocommit = True

        cursor = conn.cursor()

        row = cursor.execute('''select id from toutiao_news_latest where url='{}';'''.format(result['url']))

        if row == 0:

            sql = '''insert into toutiao_news_test(title,news_time,url,from_source,author,news_type,digest,contents,commentCount,image_url,check_status,tag) values ('{}','{}','{}','{}','{}','{}','{}', '{}','{}','{}','{}','{}');'''.format(
                result['title'].replace(chr(39), "\\'"), result['ptime'], result['url'], result['source'],
                result['editor'], result['new_type'], result['digest'], result['content'].replace(chr(39), "\\'"),
                result['commentCount'], result['imgsrc'], '0', result['new_id'])

            cursor.execute(sql)
            conn.commit()

            print("数据保存成功")

    except Exception as e:
        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    url = 'https://www.toutiao.com/ch/news_entertainment/'
    # url = 'https://www.toutiao.com/ch/selected/'
    ttapi(url)
