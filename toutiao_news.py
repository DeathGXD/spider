"""
APP爬虫：
一般APP端的爬虫要比网页端简单一些，所以遇到网页端数据较难爬取时，可以考虑从APP端入手。
国家信息公示系统：
    网页端：js加密，需要动态获取cookie，__jsl__；
    APP端：不需要任何js解密，直接发送一个请求就可以获取到数据；
今日头条：
    网页端：js加密，as/cp/_signature，其中_signature破解较为麻烦；
    APP端：js加密，只需要as/cp两个参数(每次都更新)，_signature参数就不是必须要携带的；
"""
import time, requests, hashlib, json


def get_as_cp():
    """
    手机端：
        function r() {
            var e = Math.floor((new Date).getTime() / 1e3)
              , t = e.toString(16).toUpperCase()
              , n = o(e).toString().toUpperCase();
            if (8 !== t.length)
                return {
                    as: "479BB4B7254C150",
                    cp: "7E0AC8874BB0985"
                };
            for (var r = n.slice(0, 5), i = n.slice(-5), a = "", s = 0; s < 5; s++)
                a += r[s] + t[s];
            for (var u = "", l = 0; l < 5; l++)
                u += t[l + 3] + i[l];
            return {
                as: "A1" + a + t.slice(-3),
                cp: t.slice(0, 3) + u + "E1"
            }
        }
    网页端：
        e.getHoney = function() {
            var t = Math.floor((new Date).getTime() / 1e3)
              , e = t.toString(16).toUpperCase()
              , i = md5(t).toString().toUpperCase();
            if (8 != e.length)
                return {
                    as: "479BB4B7254C150",
                    cp: "7E0AC8874BB0985"
                };
            for (var n = i.slice(0, 5), a = i.slice(-5), s = "", o = 0; 5 > o; o++)
                s += n[o] + e[o];
            for (var r = "", c = 0; 5 > c; c++)
                r += e[c + 3] + a[c];
            return {
                as: "A1" + s + e.slice(-3),
                cp: e.slice(0, 3) + r + "E1"
            }
        }
    :return:
    """

    # 1. 先得到一个整数的时间戳，round()是对小数进行四舍五入，得到一个整数
    t = round(time.time())
    # 2. 将这个整数类型的时间戳，转化为十六进制的字符串，并且将字符串全部转化为大写
    # hex()内置函数，用于将一个整数转化为16进制的字符串，对应的是js中的toString(16)
    e = hex(t).upper().replace('0X', '')
    # 3. 经过分析发现：i = md5(t).toString().toUpperCase();比n = o(e).toString().toUpperCase();简单。
    md = hashlib.md5()
    # 注意：update的参数一定是一个字节类型(bytes)的数据
    md.update(str(t).encode('utf8'))
    i = md.hexdigest().upper()
    # 4. 判断条件
    if len(e) != 8:
        return {
            "as": "479BB4B7254C150",
            "cp": "7E0AC8874BB0985"
        }
    # 5. 还原这两个for循环
    """
    i = F74F9D099F994027DDFFEAA29C92323B
    slice(0, 5)等价于python中的 [0:5] 切片操作
    var n = i.slice(0, 5);
    var a = i.slice(-5);
    var s = "";
    var r = "";

    for (var o = 0; 5 > o; o++)
        s += n[o] + e[o];
    for (var c = 0; 5 > c; c++)
        r += e[c + 3] + a[c];
    return {
        as: "A1" + s + e.slice(-3),
        cp: e.slice(0, 3) + r + "E1"
    }
    """
    # 从i这个字符串的前面切5个字符得到n，再从后面切5个得到a。
    n = i[0:5]
    a = i[-5:]
    s = ""
    r = ""

    for num in range(5):
        s += n[num] + e[num]

    for num in range(5):
        r += e[num + 3] + a[num]
    return {
        "as": "A1" + s + e[-3:],
        "cp": e[0:3] + r + "E1"
    }


def get_list_json(data_dict):
    t = round(time.time())
    print(t)
    # max_behot_time这个参数就是用来控制翻页的一个时间戳，每一页请求完以后，将最后一条数据的behot_time值获取出来作为下一次请求的参数即可。
    api_url = 'https://m.toutiao.com/list/?tag=news_hot&ac=wap&count=20&format=json_raw&as={}&cp={}&max_behot_time={}&i={}'.format(
        data_dict['as'], data_dict['cp'], t, t)
    response = requests.get(api_url, headers={
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'})
    if response.status_code == 200:
        print(response.text)
        print(json.loads(response.text))
        print(len(json.loads(response.text)))


if __name__ == '__main__':
    result = get_as_cp()
    get_list_json(result)