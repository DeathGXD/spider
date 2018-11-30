#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-11-29 08:49:04
# Project: test2

from pyspider.libs.base_handler import *
from urllib import request
import json
import requests
import os


class Handler(BaseHandler):
    crawl_config = {}

    
    def pasre_url(self):
        self.crawl_config[news_type]
        

        ### https://blog.csdn.net/sgl520lxl/article/details/81938662

        result=str(respoen, encoding = "utf-8")[9:-1]

        url='https://3g.163.com/touch/reconstruct/article/list/BBM54PGAwangning/10-10.html'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://3g.163.com/touch/reconstruct/article/list/BBM54PGAwangning/10-10.html', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        self.crawl('https://3g.163.com/touch/reconstruct/article/list/BBM54PGAwangning/10-10.html', callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "data":response.json['artiList']['BBM54PGAwangning']['digest'],
        }
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
