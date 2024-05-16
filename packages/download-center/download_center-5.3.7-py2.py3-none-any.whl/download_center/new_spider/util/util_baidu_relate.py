# -*- coding: utf8 -*-
import os
import string
import sys
import random
import base64
import time
import traceback
import uuid
import urllib
import urllib.parse
from http import cookiejar
from urllib.request import Request, HTTPCookieProcessor, build_opener

import requests


class UtilBaiduRelate(object):

    def __init__(self, remote=True):
        pass


    # 获取移动端ua
    def get_mobile_useragent(self):
        mobile_useragent_list = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/533.36",
            "Mozilla/5.0 (Linux; U; Android 5.0.2; zh-CN; Letv X501 Build/DBXCNOP5501304131S) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.10.0.800 U3/0.8.0 Mobile Safari/534.30",
            "Mozilla/5.0 (Linux; U; Android 5.0.2; zh-cn; Letv X501 Build/DBXCNOP5501304131S) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.7 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3 baiduboxapp/7.3.1 (Baidu; P1 5.1.1)",
            "Mozilla/5.0 (Linux; U; Android 4.3; zh-cn; N5117 Build/JLS36C) AppleWebKit/534.24 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.24 T5/2.0 baiduboxapp/7.0 (Baidu; P1 4.3)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/13D15 UCBrowser/10.9.15.793 Mobile",
            "Mozilla/5.0 (iPhone 6p; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/6.0 MQQBrowser/6.7 Mobile/13D15 Safari/8536.25 MttCustomUA/2",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13D15 Safari/601.1",
            "Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; GT-S7572 Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.7 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; SM-J3109 Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.6 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; Coolpad 8297-T01 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.6 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; MX4 Pro Build/LMY48W) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.10.0.800 U3/0.8.0 Mobile Safari/534.30",
            "Mozilla/5.0 (Linux; Android 5.1; m2 note Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.114 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; m2 note Build/LMY47D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.9.10.788 U3/0.8.0 Mobile Safari/534.30",
            "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; m2 note Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.6 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; CHM-CL00 Build/CHM-CL00) AppleWebKit/534.24 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.24 T5/2.0 baiduboxapp/7.1 (Baidu; P1 4.4.4)",
            "Mozilla/5.0 (Linux; Android 5.0.1; HUAWEI GRA-TL00 Build/HUAWEIGRA-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36 MxBrowser/4.5.9.3000",
            "Mozilla/5.0 (Linux; Android 5.0.1; HUAWEI GRA-CL00 Build/HUAWEIGRA-CL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3 baiduboxapp/7.3.1 (Baidu; P1 5.0.1)",
            "Mozilla/5.0 (Linux; Android 5.0.2; Redmi Note 2 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3 baiduboxapp/7.3.1 (Baidu; P1 5.0.2)",
            "Mozilla/5.0 (Linux; Android 4.4.4; Che1-CL10 Build/Che1-CL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3 baiduboxapp/7.3.1 (Baidu; P1 4.4.4)",
            "Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; HUAWEI P6-C00 Build/HuaweiP6-C00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.7 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 4.3; R7007 Build/JLS36C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3 baiduboxapp/7.3.1 (Baidu; P1 4.3)",
            "Mozilla/5.0 (Linux; Android 5.1.1; KIW-CL00 Build/HONORKIW-CL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/7.1 baidubrowser/7.1.12.0 (Baidu; P1 5.1.1)",
        ]
        return random.choice(mobile_useragent_list)

    # 获取pc端ua
    def get_pc_useragent(self):
        pc_useragent_list = [
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1",
            "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        ]
        return random.choice(pc_useragent_list)

    def getBaiduPcHeader(self):
        headers = {
            "User-Agent": self.get_pc_useragent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language':'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7,ar-XB;q=0.6,ar;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': self.get_baidu_pc_cookie()
        }

        return headers

    def getBaiduMbHeader(self):
        headers = {
            "User-Agent": self.get_mobile_useragent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language':'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7,ar-XB;q=0.6,ar;q=0.5',
            'Accept-Encoding':'gzip, deflate, br',
            'Cookie': self.get_baidu_mb_cookie()
        }

        return headers

    # 获取百度移动端cookie
    def get_baidu_mb_cookie(self):
        cookies = None
        try:
            cookie_jar = cookiejar.CookieJar()
            request = Request('https://m.baidu.com/tc?tcreq4log=1', headers={})
            handlers = [HTTPCookieProcessor(cookie_jar)]
            opener = build_opener(*handlers)
            opener.open(request, timeout=10)
            for cookie in cookie_jar:
                if cookie.name == 'BDORZ':
                    cookies = 'BDORZ=' + cookie.value
                    break
        except Exception:
            pass
        return cookies

        # 获取百度pc 端cookie

    def get_baidu_pc_cookie(self):
        letters_one = []
        letters_two = []
        for _ in range(32):
            letters_one.append(random.choice(string.ascii_uppercase + string.digits))

        for _ in range(27):
            letters_two.append(random.choice(string.ascii_lowercase + string.digits))

        return 'BAIDUID=%s:FG=1' % (''.join(letters_one)) + '; ' + 'BA_HECTOR=%s' % (''.join(letters_two))


    def get_real_url(self, baidu_url,try_count=1, timeout=5):
        max_retry_num = 3
        if try_count > max_retry_num:
            return ''

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
        try:
            response = requests.get(baidu_url, headers=headers, timeout=timeout, allow_redirects=False)
            if response.status_code == 302:
                return response.headers['Location']
            elif response.status_code == 200:
                res = requests.get(baidu_url, headers=headers, timeout=timeout, allow_redirects=True)
                return res.url
            else:
                return self.get_real_url(baidu_url, try_count + 1)
                # return ''
        except Exception as err:
            return self.get_real_url(baidu_url, try_count + 1)
            # return ''

    def generate_weixin_user_agent(self):
        iOS_version_random = random.randint(12, 15)
        android_version_random = random.randint(8, 12)

        uas = [
            f'Mozilla/5.0 (Linux; Android {android_version_random}; RMX3115 Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3225 MMWEBSDK/20220402 Mobile Safari/537.36 MMWEBID/7093 MicroMessenger/8.0.22.2140(0x2800{android_version_random}E6) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64',
            f'Mozilla/5.0 (iPhone; CPU iPhone OS {iOS_version_random}_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/{iOS_version_random}E148 MicroMessenger/8.0.22(0x1800{iOS_version_random}28) NetType/WIFI Language/zh_CN',
            f'Mozilla/5.0 (Linux; Android {android_version_random}; M2007J1SC Build/QKQ1.200419.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3225 MMWEBSDK/20220402 Mobile Safari/537.36 MMWEBID/2728 MicroMessenger/8.0.22.2140(0x2800{android_version_random}F2) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64'
        ]
        return random.choice(uas)

    #获取详情页百家号cookie
    def get_baijiahao_cookie(self):
        url = 'http://124.220.177.240:5022/baijiahao/random'
        ddd = requests.get(url).json()
        line = ''
        for k, v in ddd.items():
            line += f'{k}={v}; '
        # print(line)
        return line

def test():
    untilBaidu = UtilBaiduRelate()
    print(untilBaidu.getBaiduPcHeader())

if __name__ == '__main__':
    test()