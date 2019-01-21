#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from urllib import request
import json
import pymysql
from bs4 import BeautifulSoup
import requests
import traceback


def parse_url():
    news_type = '{"news_type": [{"name": "推荐", "id": "BA8J7DG9wangning"}]}'
    news = json.loads(news_type)

    for data in news['news_type']:

        for i in range(0, 100, 1):
            for j in range(1, 21, 1):
                url = 'https://3g.163.com/touch/reconstruct/article/list/%s/%d-%d.html' % (data['id'], i, j)
                print(url)
                request_data(url, data['id'], data['name'])


def request_data(url=None, id=None, name=None):
    try:
        header = {
            'Accept-Charset': 'UTF-8',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'vjuids=-7a4563b9.1653556d662.0.7fdee0f2bc22a; _ntes_nnid=7d9dc0dec6548bacf9960702c1bc9ee0,1534198208121; _ntes_nuid=7d9dc0dec6548bacf9960702c1bc9ee0; __gads=ID=f08dbcff9cc85b40:T=1534144217:S=ALNI_MZAduzhcd2yULxO8B8ol10pZrELXA; UM_distinctid=165d184bfe654e-0c86f82c2ba54-61547428-100200-165d184bfe722e; usertrack=ezq0o1vD4RccepHSl7ADAg==; hb_MA-A924-182E1997E62F_source=172.16.25.72%3A5000; mp_MA-A924-182E1997E62F_hubble=%7B%22sessionReferrer%22%3A%20%22http%3A%2F%2Fbj.house.163.com%2F%3Fqstr%3D%22%2C%22updatedTime%22%3A%201541579766562%2C%22sessionStartTime%22%3A%201541579766552%2C%22deviceUdid%22%3A%20%2280ee3ba7-0103-425e-94af-176f50ea570a%22%2C%22persistedTime%22%3A%201541579766544%2C%22LASTEVENT%22%3A%20%7B%22eventId%22%3A%20%22househome%22%2C%22time%22%3A%201541579766562%7D%2C%22sessionUuid%22%3A%20%228fa2e272-060a-4d08-8779-7b4bc52b0c7f%22%7D; __f_=1541581502682; mail_psc_fingerprint=d80b3cb4cb348c84c998dc9b6997bdbd; Province=021; City=021; _antanalysis_s_id=1542695162868; hb_MA-BFF5-63705950A31C_source=172.16.25.72%3A5000; vjlast=1534198208.1543386830.11; NNSSPID=cd86c3ac37c54d049b53f637fc224bff; ne_analysis_trace_id=1543393250323; pgr_n_f_l_n3=29aa9bad2ea04a5015433931967807731; s_n_f_l_n3=29aa9bad2ea04a501543396871923; vinfo_n_f_l_n3=29aa9bad2ea04a50.1.23.1534198208162.1543393656200.1543396872633; mp_MA-B4F0-3EDB3213C01D_hubble=%7B%22sessionReferrer%22%3A%20%22%22%2C%22updatedTime%22%3A%201543454550181%2C%22sessionStartTime%22%3A%201543454461691%2C%22deviceUdid%22%3A%20%225c5032a1-3284-48d1-b0b5-4932bd3dc818%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referring_domain%22%3A%20%22%24direct%22%2C%22persistedTime%22%3A%201543454461684%2C%22LASTEVENT%22%3A%20%7B%22eventId%22%3A%20%22da_screen%22%2C%22time%22%3A%201543454550181%7D%2C%22sessionUuid%22%3A%20%22d011a078-aaee-45d7-92a2-82a7dfed3a08%22%7D',
            'Host': '3g.163.com',
            'Referer': 'https://3g.163.com/touch/news/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3554.0 Mobile Safari/537.36'
        }

        data = None

        rq = request.Request(url, data=data, headers=header)
        res = request.urlopen(rq)
        respoen = res.read()
        result = str(respoen, encoding="utf-8")[9:-1]
        news_data = json.loads(result)

        for newdata in news_data[id]:

            newdata['new_type'] = name
            newdata['new_id'] = id

            if newdata['digest'] != "" and newdata['digest'] != "#" and newdata['url'] != "" and newdata['url'] != None and len(newdata['url']) < 60 and newdata['imgsrc'] != "":

                html = requests.get(newdata['url']).text

                soup = BeautifulSoup(html, "html.parser")

                imageurl = ''
                count = 0

                if len(soup.find_all('img')) > 4:
                    for img in soup.find_all('img'):
                        imgurl = img.get('data-src')

                        if count < 3 and not imgurl.endswith('html'):
                            imageurl = imgurl + ',' + imageurl
                            count = count + 1

                    newdata['imgsrc'] = imageurl

                newdata['content'] = str(soup.find_all(class_='content')[0])
                newdata['editor'] = str(soup.find_all(class_='editor')[0].string)

                on_result(newdata)
    except Exception:
        print("抓取数据错误")

def on_result(result=None):
    print(result)
    try:
        conn = pymysql.connect(host="47.101.146.57", port=2018, user="root", password="Liuku!!!111",
                                    db="dm_report", charset='utf8')
        conn.autocommit = True

        cursor = conn.cursor()

        row = cursor.execute('''select id from toutiao_news where url='{}';'''.format(result['url']))

        if row == 0:

            sql = '''insert into toutiao_news(title,news_time,url,from_source,author,news_type,digest,contents,commentCount,image_url,check_status,tag) values ('{}','{}','{}','{}','{}','{}','{}', '{}','{}','{}','{}','{}');'''.format(
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
    while True:
        parse_url()




