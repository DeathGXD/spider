#!/usr/bin/python3

from urllib import request
import json
#import requests
import os

def parse_url():
    news_type = '{"news_type": [{"name": "推荐", "id": "BA8J7DG9wangning"},{"name": "军事", "id": "BAI67OGGwangning"},{"name": "公开课", "id": "DJFFJBSLlizhenzhen"},{"name": "社会", "id": "BCR1UC1Qwangning"},{"name": "国内", "id": "BD29LPUBwangning"},{"name": "国际", "id": "BD29MJTVwangning"}]}'

    news = json.loads(news_type)



#    print(len(news['news_type']))
#    print(news['news_type'][1]['name'])

    for data in news['news_type']:

      #  print(data['name'])
      #  print(data['id'])

        for i in range(0, 100, 10):
            url = 'https://3g.163.com/touch/reconstruct/article/list/%s/%d-10.html' % (data['id'], i)
          #  print(url)
            request_data(url)





def request_data(url):
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
    cl = json.loads(result)

    print(cl)



if __name__ == '__main__':
    parse_url()




