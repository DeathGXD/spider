#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import json
import pymysql
import traceback


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