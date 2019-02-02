#!/usr/bin/python3
#!coding=utf-8

import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json
import time
from urllib import request
import urllib3



def jsonParse():
    data = "{\"abstract\":\"肝脏是人体非常重要的一个器官，肝脏能起到非常大的解毒作用。如果人体的肝脏功能不好的话，那么身体里面的一些毒素就无法排出去，久而久也会出现一些中毒的症状。\",\"action_list\":[{\"action\":1,\"desc\":\"\",\"extra\":{}},{\"action\":3,\"desc\":\"\",\"extra\":{}},{\"action\":7,\"desc\":\"\",\"extra\":{}},{\"action\":9,\"desc\":\"\",\"extra\":{}}],\"aggr_type\":1,\"allow_download\":false,\"article_sub_type\":0,\"article_type\":0,\"article_url\":\"http://toutiao.com/group/6649155791372698119/\",\"article_version\":0,\"ban_comment\":0,\"behot_time\":1548230017,\"bury_count\":0,\"cell_flag\":262155,\"cell_layout_style\":1,\"cell_type\":0,\"comment_count\":0,\"content_decoration\":\"\",\"cursor\":1548230017000,\"digg_count\":1,\"display_url\":\"http://toutiao.com/group/6649155791372698119/\",\"filter_words\":[{\"id\":\"8:0\",\"is_selected\":false,\"name\":\"看过了\"},{\"id\":\"9:1\",\"is_selected\":false,\"name\":\"内容太水\"},{\"id\":\"5:39339291\",\"is_selected\":false,\"name\":\"拉黑作者:家庭医生在线网\"},{\"id\":\"2:31135323\",\"is_selected\":false,\"name\":\"不想看:养生\"},{\"id\":\"6:16375\",\"is_selected\":false,\"name\":\"不想看:肝脏\"}],\"forward_info\":{\"forward_count\":0},\"gallary_image_count\":3,\"group_id\":6649155791372698119,\"has_image\":true,\"has_m3u8_video\":false,\"has_mp4_video\":0,\"has_video\":false,\"hot\":0,\"ignore_web_transform\":1,\"image_list\":[{\"height\":575,\"uri\":\"list/dfic-imagehandler/f9b7f730-1734-4e37-9784-ff5769eaa465\",\"url\":\"http://p1-tt.bytecdn.cn/list/300x196/dfic-imagehandler/f9b7f730-1734-4e37-9784-ff5769eaa465.webp\",\"url_list\":[{\"url\":\"http://p1-tt.bytecdn.cn/list/300x196/dfic-imagehandler/f9b7f730-1734-4e37-9784-ff5769eaa465.webp\"},{\"url\":\"http://p9-tt.bytecdn.cn/list/300x196/dfic-imagehandler/f9b7f730-1734-4e37-9784-ff5769eaa465.webp\"},{\"url\":\"http://p3-tt.bytecdn.cn/list/300x196/dfic-imagehandler/f9b7f730-1734-4e37-9784-ff5769eaa465.webp\"}],\"width\":1023},{\"height\":675,\"uri\":\"list/dfic-imagehandler/46622e05-56ff-4ed1-b657-b6b5a16daaac\",\"url\":\"http://p3-tt.bytecdn.cn/list/300x196/dfic-imagehandler/46622e05-56ff-4ed1-b657-b6b5a16daaac.webp\",\"url_list\":[{\"url\":\"http://p3-tt.bytecdn.cn/list/300x196/dfic-imagehandler/46622e05-56ff-4ed1-b657-b6b5a16daaac.webp\"},{\"url\":\"http://p9-tt.bytecdn.cn/list/300x196/dfic-imagehandler/46622e05-56ff-4ed1-b657-b6b5a16daaac.webp\"},{\"url\":\"http://p1-tt.bytecdn.cn/list/300x196/dfic-imagehandler/46622e05-56ff-4ed1-b657-b6b5a16daaac.webp\"}],\"width\":1200},{\"height\":675,\"uri\":\"list/dfic-imagehandler/07b6b1e2-a979-4af4-a681-5e5ef8c959f6\",\"url\":\"http://p9-tt.bytecdn.cn/list/300x196/dfic-imagehandler/07b6b1e2-a979-4af4-a681-5e5ef8c959f6.webp\",\"url_list\":[{\"url\":\"http://p9-tt.bytecdn.cn/list/300x196/dfic-imagehandler/07b6b1e2-a979-4af4-a681-5e5ef8c959f6.webp\"},{\"url\":\"http://p1-tt.bytecdn.cn/list/300x196/dfic-imagehandler/07b6b1e2-a979-4af4-a681-5e5ef8c959f6.webp\"},{\"url\":\"http://p9-tt.bytecdn.cn/list/300x196/dfic-imagehandler/07b6b1e2-a979-4af4-a681-5e5ef8c959f6.webp\"}],\"width\":1200}],\"interaction_data\":\"\",\"is_subject\":false,\"item_id\":6649155791372698119,\"item_version\":0,\"keywords\":\"唇色发黑,早上起床,肝脏功能不好,眼睛,人体\",\"level\":0,\"log_pb\":{\"impr_id\":\"20190123161607010023075223047865D\",\"is_following\":\"0\"},\"media_info\":{\"avatar_url\":\"http://p1.pstatp.com/large/123200176d3c39c0cfda\",\"follow\":false,\"is_star_user\":false,\"media_id\":1554938722203650,\"name\":\"家庭医生在线网\",\"recommend_reason\":\"\",\"recommend_type\":0,\"user_id\":53324103362,\"user_verified\":true,\"verified_content\":\"\"},\"media_name\":\"家庭医生在线网\",\"middle_image\":{\"height\":575,\"uri\":\"list/dfic-imagehandler/f9b7f730-1734-4e37-9784-ff5769eaa465\",\"url\":\"http://p1-tt.bytecdn.cn/list/300x196/dfic-imagehandler/f9b7f730-1734-4e37-9784-ff5769eaa465.webp\",\"url_list\":[{\"url\":\"http://p1-tt.bytecdn.cn/list/300x196/dfic-imagehandler/f9b7f730-1734-4e37-9784-ff5769eaa465.webp\"},{\"url\":\"http://p3-tt.bytecdn.cn/list/300x196/dfic-imagehandler/f9b7f730-1734-4e37-9784-ff5769eaa465.webp\"},{\"url\":\"http://p9-tt.bytecdn.cn/list/300x196/dfic-imagehandler/f9b7f730-1734-4e37-9784-ff5769eaa465.webp\"}],\"width\":1023},\"need_client_impr_recycle\":1,\"publish_time\":1548129107,\"read_count\":531,\"repin_count\":2,\"rid\":\"20190123161607010023075223047865D\",\"share_count\":0,\"share_info\":{\"cover_image\":null,\"description\":null,\"on_suppress\":0,\"share_type\":{\"pyq\":0,\"qq\":0,\"qzone\":0,\"wx\":0},\"share_url\":\"http://m.toutiao.com/a6649155791372698119/?iid=0\\u0026app=news_article\\u0026is_hit_share_recommend=0\",\"title\":\"晨起有这3个表现，是肝脏在向你报告：我生病了\",\"token_type\":1,\"weixin_cover_image\":{\"height\":1229,\"uri\":\"large/tos-cn-i-0000/0f9d6d0c-1df9-11e9-9893-0cc47a930ee4\",\"url\":\"http://p3-tt.bytecdn.cn/large/tos-cn-i-0000/0f9d6d0c-1df9-11e9-9893-0cc47a930ee4\",\"url_list\":[{\"url\":\"http://p3-tt.bytecdn.cn/large/tos-cn-i-0000/0f9d6d0c-1df9-11e9-9893-0cc47a930ee4\"},{\"url\":\"http://p9-tt.bytecdn.cn/large/tos-cn-i-0000/0f9d6d0c-1df9-11e9-9893-0cc47a930ee4\"},{\"url\":\"http://p3-tt.bytecdn.cn/large/tos-cn-i-0000/0f9d6d0c-1df9-11e9-9893-0cc47a930ee4\"}],\"width\":1023}},\"share_url\":\"http://m.toutiao.com/a6649155791372698119/?iid=0\\u0026app=news_article\\u0026is_hit_share_recommend=0\",\"show_dislike\":true,\"show_portrait\":false,\"show_portrait_article\":false,\"source\":\"家庭医生在线网\",\"source_icon_style\":4,\"source_open_url\":\"sslocal://profile?uid=53324103362\",\"tag\":\"news_health\",\"tag_id\":6649155791372698119,\"tip\":0,\"title\":\"晨起有这3个表现，是肝脏在向你报告：我生病了\",\"ugc_recommend\":{\"activity\":\"\",\"reason\":\"青云计划获奖者 优质健康领域创作者\"},\"url\":\"http://toutiao.com/group/6649155791372698119/\",\"user_info\":{\"avatar_url\":\"http://p1.pstatp.com/thumb/123200176d3c39c0cfda\",\"description\":\"由院士及国医大师指导，专注生产健康内容，做千家万户的家庭医生\",\"follow\":false,\"follower_count\":0,\"live_info_type\":1,\"name\":\"家庭医生在线网\",\"schema\":\"sslocal://profile?uid=53324103362\\u0026refer=all\",\"user_auth_info\":\"{\\\"auth_type\\\":\\\"0\\\",\\\"auth_info\\\":\\\"青云计划获奖者 优质健康领域创作者\\\",\\\"other_auth\\\":{\\\"interest\\\":\\\"优质健康领域创作者\\\"}}\",\"user_id\":53324103362,\"user_verified\":true,\"verified_content\":\"青云计划获奖者 优质健康领域创作者\"},\"user_repin\":0,\"user_verified\":1,\"verified_content\":\"青云计划获奖者 优质健康领域创作者\",\"video_style\":0}"

    content = json.loads(data)

    print(len(content['image_list']))

    if('video_detail_info' in content):
        print("you")
    else:
        print("mei")

    # imgsrc = ''
    # for img in content['image_list']:
    #     imgsrc = imgsrc + img['url'] + ','
    #
    # print(imgsrc)

def htmlParse():

    mobile_emulation = {"deviceName": "iPhone X"}
    options = Options()
    options.add_argument('-headless')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36')
    # options.set_capability("deviceName", "iPhone 6")

    driver = webdriver.Firefox(executable_path='D:\geckodriver\geckodriver.exe', options=options)
    driver.get("https://m.toutiao.com/i6650068596946895367/")
    source = driver.page_source
    print(source)
    soup = BeautifulSoup(source, "html.parser")
    divs = soup.find_all(id_='article_content')
    print(divs)


def requestTime():
    t2 = int(time.time()) -600
    t = int(time.time())
    print(int(t / 1000) * 1000)

    print(t2)

def getData():
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

    url='https://www.toutiao.com/api/pc/feed/?min_behot_time=0&category=__all__'
    data = None
    rq = request.Request(url, data=data, headers=header)
    res = request.urlopen(rq)
    respoen = res.read()
    result = str(respoen, encoding="utf-8")
    news_data = json.loads(result)
    d = news_data['data']
    print(d)
    print(len(d))

    for da in d:
        print(da['abstract'])
        print(da['tag'])
        print(da['comments_count'])
        print(da['tag_url'])
        print(da['title'])
        print(da['chinese_tag'])
        print(da['source'])
        print(da['image_url'])
        print(da['source_url'])
        print(da['item_id'])
        print(da['behot_time'])


def getHtml():
    # page = urllib3
    page = request.urlopen('https://www.toutiao.com/a6651506811981529612/')

    # html = page.read().decode('utf-8')

    print(page)

    content = requests.get('https://www.toutiao.com/a6651506811981529612/')
    print(content)


if __name__ == '__main__':
    # print(len('/group/6647293254217761287/'))
    # https: // www.toutiao.com / api / pc / feed /

    # htmlParse()
    # getData()
    # jsonParse()
    requestTime()
    # getHtml()