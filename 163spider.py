#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-11-26 16:52:53
# Project: toutiao_news

from pyspider.libs.base_handler import *
import pymysql


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.conn = pymysql.connect(host="47.101.146.57", port=2018, user="root", password="Liuku!!!111",
                                    db="dm_report", charset='utf8')
        self.conn.autocommit = True
        print("已打开数据库链接")
        self.crawl('https://www.163.com/', callback=self.index_page)

    def on_finished(self):
        if hasattr(self, 'conn'):
            self.conn.close()
            print("数据库链接已关闭！")

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            html = each.attr.href[-5:]
            if 'htm' in html:
                self.crawl(each.attr.href, callback=self.detail_page)
            else:
                continue

        if response.doc('a[href^="http"]').items() != None:
            for each in response.doc('a[href^="http"]').items():
                self.crawl(each.attr.href, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "content": response.doc('.post_text').html(),
            "news_time": response.doc('.post_time_source').text()[:19],
            "from_source": response.doc('.post_time_source a').text(),
            "author": response.doc('.ep-editor').text(),
            "news_type": response.doc('.post_crumb a').text()[4:7],
            "image_url": response.doc('.f_center img').attr('src'),
        }

    def on_result(self, result):
        if not hasattr(self, 'conn'):
            self.conn = pymysql.connect(host="47.101.146.57", port=2018, user="root", password="Liuku!!!111",
                                        db="dm_report", charset='utf8')
            self.conn.autocommit = True
            print("已重新获取数据库链接")

        if not result or not result['content']:
            return

        cursor = self.conn.cursor()
        sql = '''insert into toutiao_news(title,news_time,url,from_source,author,news_type,contents,image_url,check_status) values ('{}','{}','{}','{}','{}','{}','{}', '{}','{}');'''.format(
            result['title'].replace(chr(39), "\\'"), result['news_time'], result['url'], result['from_source'],
            result['author'], result['news_type'], result['content'].replace(chr(39), "\\'"), result['image_url'], '0')
        print(sql)
        cursor.execute(sql)
        self.conn.commit()
        cursor.close()
        print("数据保存成功")























