#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from urllib import request
import json
import time
import pymysql
from bs4 import BeautifulSoup
import requests
import traceback
import pymysql
import traceback
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def start():
    news_type = '{"news_type":[{"type":"news_entertainment","name":"娱乐","id":"BA10TA81wangning"},' + \
                    '{"type":"news_tech","name":"科技","id":"BA8D4A3Rwangning"},' + \
                    '{"type":"news_game","name":"游戏","id":"BA9D4A3Rtoutiao"},' + \
                    '{"type":"news_sports","name":"体育","id":"BA8E6OEOwangning"},' + \
                    '{"type":"news_car","name":"汽车","id":"BA8DOPCSwangning"},' + \
                    '{"type":"news_finance","name":"财经","id":"BA8EE5GMwangning"},' + \
                    '{"type":"funny","name":"搞笑","id":"BD21K0DLtoutiao"},' + \
                    '{"type":"news_military","name":"军事","id":"BAI67OGGwangning"},' + \
                    '{"type":"news_world","name":"国际","id":"BD29MJTVwangning"},' + \
                    '{"type":"news_fashion","name":"时尚","id":"BA8F6ICNwangning"},' + \
                    '{"type":"news_travel","name":"旅游","id":"BEO4GINLwangning"},' + \
                    '{"type":"news_baby","name":"亲子","id":"BEO4PONRwangning"},' + \
                    '{"type":"news_discovery","name":"探索","id":"BEO4PONRtoutiao"},' + \
                    '{"type":"news_regimen","name":"养生","id":"BAI6I0Otoutiao"},' + \
                    '{"type":"news_essay","name":"美文","id":"BA09taitoutiao"},' + \
                    '{"type":"news_history","name":"历史","id":"C275ML7Gwangning"},' + \
                    '{"type":"news_food","name":"美食","id":"BDC4QSV3toutiao"}]}'

    news = json.loads(news_type)

    for data in news['news_type']:
        url = 'https://www.toutiao.com/api/pc/feed/?min_behot_time=0&category=%s' % data['type']
        print(url)
        request_data(url, data['name'], data['id'])


def request_data(url=None, name=None, id=None):
    driver = web_driver()

    try:

        header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Accept-Charset': 'UTF-8',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Cache-Control': 'max-age=0',
                  'Connection': 'keep-alive',
                  'Cookie': 'csrftoken=186f69db19b65ffe788fe1caa7080e06; tt_webid=6613248121868895752; tt_webid=6613248121868895752; UM_distinctid=167302a28300-06596aa01a4775-75133b4f-100200-167302a28383d5; WEATHER_CITY=%E5%8C%97%E4%BA%AC; CNZZDATA1259612802=56902657-1542698355-https%253A%252F%252Fwww.baidu.com%252F%7C1543191469',
                  'Host': 'www.toutiao.com',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3554.0 Mobile Safari/537.36'
                  }

        data = None

        rq = request.Request(url, data=data, headers=header)
        res = request.urlopen(rq)
        respoen = res.read()
        result = str(respoen, encoding="utf-8")
        news_data = json.loads(result)['data']

        for news in news_data:
            url = news['source_url']

            # if len(url) > 27:
            #     continue

            url = 'https://toutiao.com' + url
            print(url)
            driver.get(url)
            source = driver.page_source

            soup = BeautifulSoup(source, "html.parser")
            if len(soup.find_all(class_='article-content')) != 0:
                news['content'] = str(soup.find_all(class_='article-content')[0])
                news['source_url'] = url

                images = ''
                if 'image_list' in news:
                    for image in news['image_list']:
                        img = 'https:' + image['url']
                        images = images + img + ','
                elif 'middle_image' in news:
                    images = news['middle_image']

                if 'comments_count' not in news:
                    news['comments_count'] = 0

                news['imgsrc'] = images
                news['ptime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(news['behot_time']))
                news['news_type'] = name
                news['news_id'] = id

                on_result(news)
            else:
                continue

        driver.quit()
    except traceback:
        traceback.print_exc()


def web_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36')
    driver = webdriver.Firefox(executable_path='D:\geckodriver\geckodriver.exe', options=options)

    return driver


def on_result(result=None):

    try:
        conn = pymysql.connect(host="47.101.146.57", port=2018, user="root", password="Liuku!!!111",
                                    db="dm_report", charset='utf8')
        conn.autocommit = True

        cursor = conn.cursor()

        row = cursor.execute('''select id from toutiao_news where url='{}';'''.format(result['source_url']))

        if row == 0:

            sql = '''insert into toutiao_news(title,news_time,url,from_source,author,news_type,digest,contents,commentCount,image_url,check_status,tag,news_id) values ('{}','{}','{}','{}','{}','{}','{}', '{}','{}','{}','{}','{}','{}');'''.format(
                result['title'].replace(chr(39), "\\'"), result['ptime'], result['source_url'], result['source'],
                result['source'], result['news_type'], result['abstract'].replace(chr(39), "\\'"), result['content'].replace(chr(39), "\\'"),
                result['comments_count'], result['imgsrc'], '0', result['news_id'],result['item_id'])
            # print(sql)

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










