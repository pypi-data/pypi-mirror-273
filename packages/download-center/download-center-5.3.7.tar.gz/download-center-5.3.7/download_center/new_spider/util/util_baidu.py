# -*- coding: utf8 -*-
"""
duquan
2019/12/19
百度移动端解析工具
"""
import json
import random
import re
import uuid

import pymysql
import requests
from lxml import etree
import redis
import time

from lxml.html import fromstring

import download_center.config as pro_config
from download_center.store import config
from http import cookiejar
from urllib.request import Request, HTTPCookieProcessor, build_opener

from pymysql.converters import escape_string


class UtilBaiduMb(object):
    def __init__(self):
        self.mobile_useragent_list = [
            "Mozilla/5.0 (Linux; U; Android 5.0.2; zh-CN; Letv X501 Build/DBXCNOP5501304131S) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.10.0.800 U3/0.8.0 Mobile Safari/534.30",
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/533.36",
            "Mozilla/5.0 (Linux; U; Android 5.0.2; zh-cn; Letv X501 Build/DBXCNOP5501304131S) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.7 Mobile Safari/537.36",
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
            "Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; HUAWEI P6-C00 Build/HuaweiP6-C00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.7 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 5.1.1; KIW-CL00 Build/HONORKIW-CL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/7.1 baidubrowser/7.1.12.0 (Baidu; P1 5.1.1)",
            "Mozilla/5.0(Linux;Android 5.1.1;OPPO A33 Build/LMY47V;wv) AppleWebKit/537.36(KHTML,link Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36 LieBaoFast/4.51.3",
            "Mozilla/5.0(Linux;U;Android 5.1.1;zh-CN;OPPO A33 Build/LMY47V) AppleWebKit/537.36(KHTML,like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.7.0.953 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 4.3; EVO Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
            "Mozilla/5.0(Linux;Android 5.1.1;OPPO A33 Build/LMY47V;wv) AppleWebKit/537.36(KHTML,link Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 7.0; FRD-AL00 Build/HUAWEIFRD-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043602 Safari/537.36 MicroMessenger/6.5.16.1120 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
            "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
            "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
            "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (Androdi; Linux armv7l; rv:5.0) Gecko/ Firefox/5.0 fennec/5.0",
            "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
            "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
            "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/14.14263",
            "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; HTC_D820u Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Mozilla/5.0 (iPhone 5SGLOBAL; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/6.0 MQQBrowser/5.6 Mobile/12A365 Safari/8536.25",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4.9 (KHTML, like Gecko) Version/6.0 Mobile/10A523 Safari/8536.25",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Coast/4.01.88243 Mobile/12A365 Safari/7534.48.3",
            "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; vivo Xplay6 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.6 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.1.944 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 MicroMessenger/6.5.9 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; YQ601 Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.4.3) WindVane/8.0.0 1080X1920 GCanvas/1.4.2.21",
            "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MI 5 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.1 Mobile Safari/537.36"
        ]

    # -  资讯
    def container_mb_zixun(self, container):
        try:
            item_list = list()
            news_list = container.xpath('.//div[contains(@class,"c-gap-inner-top-middle tts-b-item")]')
            for news in news_list:
                try:
                    title = news.xpath('string(.//h3/span)')
                    show_url = news.xpath('string(.//div[contains(@data-module,"c-sr")])')
                    baidu_url = news.xpath('./a/@href')[0]
                    real_url = self.get_real_url_by_baidu_url(baidu_url)
                    if real_url == '':
                        real_url = baidu_url
                    datas = {
                        'title': title,
                        'baidu_url': baidu_url,
                        'show_url': show_url,
                        'real_url': real_url,
                    }
                    item_list.append(datas)
                except:
                    pass
        except:
            return []
        else:
            return item_list

    # -  两行图片
    def container_mb_image(self, container):
        try:
            item_list = list()
            news_list = container.xpath('.//div[contains(@class,"c-img image-img-item")]')
            for image_list in news_list:
                try:
                    exposure = image_list.get("data-exposure", "")
                    baidu_url = json.loads(str(exposure).replace("\'", "\""))['loc']
                    title = ''
                    show_url = ''
                    real_url = baidu_url
                    datas = {
                        'title': title,
                        'baidu_url': baidu_url,
                        'show_url': show_url,
                        'real_url': real_url,
                    }
                    item_list.append(datas)
                except:
                    pass
        except:
            return []
        else:
            return item_list

    # -  视频
    def container_mb_video(self, container):
        try:
            item_list = list()
            news_list = container.xpath('.//div[contains(@class,"c-video-container")]/a')
            for video_list in news_list:
                title = video_list.xpath('string(.//div[contains(@class,"c-vid-title")])')
                baidu_url = video_list.xpath('./@href')[0]
                show_url = ""
                datalog = video_list.get("data-log", "")
                real_url = baidu_url
                try:
                    datalog = str(datalog).replace("\'", "\"")
                    sx_data = json.loads(datalog)
                    real_url = sx_data["mu"]
                except:
                    pass

                datas = {
                    'title': title,
                    'baidu_url': baidu_url,
                    'show_url': show_url,
                    'real_url': real_url,
                }
                item_list.append(datas)
        except:
            return []
        else:
            return item_list

    # 小视频
    def container_mb_small_video(self, container):
        try:
            item_list = list()
            # news_list = container.xpath('//div[@tpl="vid_pocket"]//div[@class="vid-scroll-content"]')
            news_list = container.xpath('//div[@tpl="vid_pocket"]//div[@class="c-scroll-item"]')
            for video_list in news_list:
                try:
                    see_more = video_list.xpath('.//div[@class="_v1-pF"]')
                    if not see_more:
                        title = ''.join(video_list.xpath('string(.//div[@class="vid-pocket-item"]/div[2]/div)'))
                        baidu_url = ''
                        show_url = ''.join(video_list.xpath('.//div[@class="vid-pocket-item"]/div[1]/div//span[contains(@class,"vid-info-author-name")]/text()')[0])
                        real_url = ''.join(video_list.xpath('.//a[@class="c-blocka"]/@href'))
                        datas = {
                            'title': title,
                            'baidu_url': baidu_url,
                            'show_url': show_url,
                            'real_url': real_url,
                        }
                        item_list.append(datas)
                except:
                    continue
        except:
            return []
        else:
            return item_list

    def container_mb_notes(self, container):
        try:
            item_list = list()
            news_list = container.xpath("//div[@class='text-list-inner']/div[contains(@data-module,'lgtlt')]")
            for video_list in news_list:
                title = video_list.xpath('./div/@titlehtml')
                show_desc = video_list.xpath('./div/@deschtml')
                baidu_url = video_list.xpath('./div/@rl-link-href')
                real_url = video_list.xpath('./div/@rl-link-data-click')
                show_url = ''
                if real_url:
                    data = json.loads(real_url[0])
                    show_url = data.get('src', '')
                datas = {
                    'title': title,
                    'show_desc': show_desc,
                    'baidu_url': baidu_url,
                    'show_url': show_url,
                }
                item_list.append(datas)
        except:
            return []
        else:
            return item_list

    # 直播
    def container_mb_zhibo(self, container):
        try:
            item_list = list()
            news_list = container.xpath('//div[@tpl="live_converge"]//div[@class="c-scroll-item"]')
            for video_list in news_list:
                title = video_list.xpath('string(.//span[contains(@class,"c-abstract")])')
                baidu_url = ''.join(video_list.xpath('.//a/@href'))
                show_url = ''
                datas = {
                    'title': title,
                    'baidu_url': baidu_url,
                    'show_url': show_url,
                }
                item_list.append(datas)
        except:
            return []
        else:
            return item_list

    def get_container_list(self, html):
        """获取搜索结果列表元素"""
        try:
            html_element = fromstring(html.encode('utf-8', 'ignore').decode('utf-8', 'ignore'))
            container_list = html_element.xpath('//div[@id="results"]/div[contains(@class,"c-result")]')
        except:
            return -1
        else:
            return container_list

    # def get_container_list(self, html):
    #     """获取搜索结果列表元素"""
    #     try:
    #         html_element = etree.HTML(html, etree.HTMLParser(encoding="utf-8"))
    #         container_list = html_element.xpath('//div[contains(@class,"c-result")]')
    #     except:
    #         return -1
    #     else:
    #         return container_list

    def get_rank(self, container):
        """获取排名"""
        try:
            rank = int(container.xpath('./@order')[0])
        except:
            return 0
        else:
            return rank

    def get_real_url_by_json(self, container):
        """通过json，获取真实url"""
        try:
            real_url = ""
            datalog = container.get("data-log", "")
            if datalog:
                try:
                    datalog = str(datalog).replace("\'", "\"")
                    sx_data = json.loads(datalog)
                    real_url = sx_data["mu"]
                except:
                    pass
            if real_url == "" or real_url == "notes.baidu.com":
                try:
                    article_list = container.xpath('.//article/@rl-link-href')
                    if len(article_list) > 0:
                        url = article_list[0]
                        headers = {
                            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
                        }
                        response = requests.get(url=url, headers=headers)
                        if "window.location.replace" in response.text:
                            url_list = re.findall(r'.*url=(.*?)".*', response.text)
                            if len(url_list) > 0:
                                url = url_list[0]
                                real_url = url
                except:
                    pass
        except Exception as e:
            return -1
        else:
            return real_url

    def get_real_url_by_baidu_url(self, baidu_url, try_count=1):
        """通过百度url获取真实url"""
        try:
            if try_count > 3:
                return ''
            else:
                headers = {
                    'User-Agent': random.choice(self.mobile_useragent_list),
                    "Cookie": self.get_cook()
                }
                response = requests.get(baidu_url, headers=headers, timeout=20)
                if response.status_code > 400:
                    print('获取real_url失败 - {}'.format(response.status_code))
                    return self.get_real_url_by_baidu_url(baidu_url, try_count + 1)
                return response.url
        except Exception:
            return self.get_real_url_by_baidu_url(baidu_url, try_count + 1)

    # 判断是否需要获取真实url - （需要获取真实url情况：完全匹配， show_url不是url格式）
    def check_get_real_url(self, container, real_url):
        # 取页面上的真实url
        datalog = container.get("data-log", "")
        if datalog:
            try:
                datalog = str(datalog).replace("\'", "\"")
                sx_data = json.loads(datalog)
                real_url = sx_data["mu"]
            except:
                return -1
        return real_url

    def get_baidu_url(self, container):
        """获取百度url"""
        xpath_rules = ['.//header[@class="c-gap-bottom-small"]//a[1]/@href',
                       './/div[@class="circle-sample"]//a[1]/@href',
                       './/article/@rl-link-href']
        return self.get_res_text(container, xpath_rules)

    def get_show_url(self, container):
        """获取显示url"""
        xpath_rules = [
            './/div[contains(@class,"android-text-top1")]//text()',
            './/span[contains(@class,"android-text-top1")]//text()',
            './/span[contains(@class,"c-showurl")]//text()',
            './/div[contains(@class,"c-showurl")]//text()',
            './/span[@class="c-color-gray"]//text()',
            './/div[@class="c-line-clamp1"]//text()',
        ]
        return remove_special_characters(self.get_res_text(container, xpath_rules))

    def get_show_title_mb(self, container):
        """获取标题"""
        xpath_rules = ['.//span[@class="c-line-clamp1"]//text()',
                       './/header//span[@class="c-title-text"]//text()',
                       './/span[@class="c-title-text"]//text()',
                       './/h3[@class="c-title title-con"]//text()',
                       './/span[@class="_1mmq3"]//text()',
                       './/div[@class="c-line-clamp1"][1]//text()',
                       './/div[@class="ugc-title__2ofi_"]//text()',
                       './/div[contains(@class,"c-title")]//text()',
                       '//div[@class="c-span7"]/div[contains(@class,"c-font-large")]/text()',
                       'string(//div[contains(@class,"ugc-title")])',
                       ".//div[@class='text-list-inner']/div[@class='text-item tts-b-item']"

                       ]
        return self.get_res_text_mb(container, xpath_rules)

    def get_res_text_mb(self, container, xpath_rules):
        """获取纯文本"""
        text = ""
        for rule in xpath_rules:
            text_list = container.xpath(rule)
            for i in text_list:
                text += i.strip().strip('”').strip('“')
            if text != "":
                return escape_string(text)
        return escape_string(text)

    def get_show_desc(self, container):
        """获取描述"""
        xpath_rules = ['.//div[@class="c-line-clamp3"]//text()',

                       './/span[@class="c-font-big wenda-abstract-quote"]/text()',
                       './/div[@class="c-line-clamp2"]//text()',
                       './/section//span//text()',
                       './/div[@class="c-font-medium c-color c-gap-bottom-small wenda-abstract-text wenda-abstract-singo-line c-color-link"]//text()',
                       './/div[@class="c-abstract c-gap-bottom wa-bk-polysemy-abstract c-line-clamp5"]//text()']
        return self.get_res_text(container, xpath_rules)

    def get_show_date(self, container):
        """获取显示日期"""
        xpath_rules = ['.//span[@class="c-gap-right-small"]//text()',
                       './/span[@class="c-color-gray c-gap-left normal-footer-no-shrink"]//text()',
                       './/span[@class="c-footer-showurl c-gap-left"]//text()',
                       ]
        res = self.get_res_text(container, xpath_rules)
        if "回答时间：" in res:
            return res.split("回答时间：")[-1]
        elif "发贴时间" in res:
            return res.split("发贴时间:")[-1]
        else:
            return res.replace('发布时间: ', '')

    def get_res_text(self, container, xpath_rules):
        """获取纯文本"""
        text = ""
        for rule in xpath_rules:
            text_list = container.xpath(rule)
            for i in text_list:
                text += i.strip().strip('”').strip('“')
            if text != "":
                break
        return escape_string(text)

    def get_mb_cookie(self):
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

    def get_cook(self):
        """
        获取有效的cookie
        :return:
        """
        try:
            key_name = 'mb'
            for i in range(2):
                if UtilBaiduCookie().totalCookies(key_name) > 0:
                    cookie = str(UtilBaiduCookie().getLastCookies(key_name=key_name)[0], encoding="utf-8")
                    return cookie
                else:
                    return self.get_mb_cookie()
        except:
            return self.get_mb_cookie()


class UtilBaiduPc(object):
    def get_container_list(self, html):
        """获取搜索结果列表元素"""
        try:
            # html_element = etree.HTML(html, etree.HTMLParser(encoding="utf-8"))
            # container_list = html_element.xpath('//div[@id="content_left"]/div')
            # return container_list
            html_element = fromstring(html)
            container_list = html_element.xpath('//div[@id="content_left"]/div[contains(@class,"new-pmd")]')
            return container_list
        except:
            return -1

    def get_rank(self, container):
        """获取排名"""
        try:
            rank = int(container.get('id', 0))
            return rank
        except:
            return 0

    # 最新相关信息
    def container_pc_news(self, container):
        try:
            item_list = list()
            news_list = container.xpath('//div[@tpl="news-realtime"]/div/div')
            for i in news_list:
                try:
                    a_list = i.xpath('./a')
                    if a_list:
                        title = ''.join(a_list[0].xpath('string(.)'))
                        baidu_url = a_list[0].xpath('./@href')[0]
                        try:
                            show_url = i.xpath('./span[@class="c-color-gray c-gap-left-small"]/text()')[0]
                        except:
                            show_url = i.xpath('./div/span[@class="c-color-gray"]/text()')[0]
                        datas = {
                            'title': title,
                            'baidu_url': baidu_url,
                            'show_url': show_url
                        }
                        item_list.append(datas)
                except:
                    continue
        except:
            return []
        else:
            return item_list

    # 高清在线观看
    def container_pc_video(self, html):
        try:
            item_list = list()
            video_list = json.loads(re.findall('"videoList":(\[.*?\])', html)[0])

            for i in video_list:
                title = i.get('title', '')
                baidu_url = i.get('jumpUrl', '')
                show_url = i.get('source', '')
                datas = {
                    'title': title,
                    'baidu_url': baidu_url,
                    'show_url': show_url
                }
                item_list.append(datas)
        except:
            return []
        else:
            return item_list

        # 最新相关信息

    def container_pc_tieba(self, container):
        try:
            item_list = list()
            tieba_list = container.xpath('//div[@tpl="tieba_general"]/div[@class="result c-container"]/div[contains(@class,"c-row")]')
            for i in tieba_list:
                a_list = i.xpath('./div[contains(@class,"c-span8")]')
                if a_list:
                    title = ''.join(a_list[0].xpath('string(./a)'))
                    baidu_url = a_list[0].xpath('./a/@href')[0]
                    datas = {
                        'title': title,
                        'baidu_url': baidu_url,
                    }
                    item_list.append(datas)
        except:
            return []
        else:
            return item_list

    def get_show_url(self, container):
        """获取显示url"""
        xpath_rules = [
            './/span[@class="nor-src-wrap"]//text()',
            './/div[contains(@class,"se_st_footer")]/a[1]//text()',
            './/div[@class="f13"]/a[1]/text()',
            './/span[@class="c-showurl"]//text()',
            './/a[@class="c-showurl"]/span//text()',
            './/div[@class="f13"]/span//text()',
            './/a[@class="c-showurl"]//text()',
            './/a[@class="c-showurl "]//text()',
            './/div[contains(@class,"c-showurl")]//text()',
            './/section/a/div//text()',
            'string(//div[@class="vmp-zxenterprise-new_qayMC"]/div/h3/a/@href)',
            'string(//h3[@class="c-title"]/span)'
        ]
        return remove_special_characters(self.get_res_text(container, xpath_rules))

    def get_show_title(self, container):
        """获取标题"""
        # xpath_rules = ['.//h3//text()', './/span[@class="c-title-text"]//text()',
        #                './/div[@class="wenda-abstract-showurl-title c-line-clamp1"]//text()',
        #                './/h3[@class="t c-gap-bottom-small"]//text()',
        #                '//h3[@role="text"]/span[@class="c-title-text"]//text()']
        xpath_rules = ['.//span[@class="c-title-text"]//text()', './/div[@class="c-line-clamp1"]//text()',
                       './/div[@class="c-font-medium c-color-t"]//text()',
                       './/div[@class="wenda-abstract-showurl-title c-line-clamp1"]//text()',
                       './/h3[@class="t c-gap-bottom-small"]//text()', './/h3[contains(@class,"t")]//text()',
                       'string(//span[@class="c-title-text"])', 'string(//div[@class="vmp-zxenterprise-new_qayMC"]/div/h3/a)',
                       'string(//div[@tpl="wenda_abstract_pc"]//div[contains(@class,"wenda-abstract-wrap-new")]//a)', 'string(//span[@class="c-title-text"])',
                       'string(//div[@tpl="vmp_zxenterprise_new"]//h3/a)']
        return self.get_res_text(container, xpath_rules)

    def get_show_desc(self, container):
        """获取描述"""
        try:
            des_list = container.cssselect("div.c-abstract")
            if len(des_list) > 0:
                des = self.get_text(des_list[0])
            else:
                des_list = container.cssselect("div.c-span18c-span-last")
                if len(des_list) > 0:
                    des = self.get_text(des_list[0])
                else:
                    des_list = container.cssselect("div.c-gap-top-small")
                    if des_list:
                        des = self.get_text(des_list[0])
                    else:
                        des = ''
        except:
            return ''
        else:
            return des

    def get_text(self, elem):
        rc = []
        for node in elem.itertext():
            rc.append(node.strip())
        return ''.join(rc)

    def get_baidu_url(self, container):
        """获取百度url"""
        xpath_rules = [
            './/h3[contains(@class,"t")]/a/@href',
            './/a[@class="c-showurl"]/@href',
            './/span[@class="c-showurl"]/text()',
            './/h3[@class="t c-gap-bottom-small"]/a/@href',
            './/section/a/@href',
            '//div[@tpl="ads_b2c_universal_card"]//a[@data-module="c-t"]/@href',
            '//*[@id="1"]/div/article/section/div/div[1]/a/@href',
            '//header[@class="c-gap-bottom-small"]/div/a[@class="c-blocka"]/@href',
            '//div[@tpl="wenda_abstract_pc"]//div[contains(@class,"wenda-abstract-wrap-new")]//a/@href',
            '//div[@tpl="ads_b2c_universal_card"]//header[@class="c-gap-bottom-small"]//a/@href',
            '//div[@tpl="vmp_zxenterprise_new"]//h3/a/@href'
        ]
        return self.get_res_text(container, xpath_rules)

    def get_show_date(self, container):
        """获取显示日期"""
        try:
            des_list = container.cssselect("div.c-abstract")
            if len(des_list) > 0:
                show_date_eles = des_list[0].xpath('descendant::span')
                if show_date_eles:
                    show_date = show_date_eles[0].text.strip()
                    show_date = str(show_date).split("-")[0].strip().replace(" ", "")
                else:
                    show_date = ''
            else:
                des_list = container.cssselect("div.c-span18c-span-last")
                if len(des_list) > 0:
                    show_date_eles = des_list[0].xpath('descendant::span[@class="m"]')
                    if show_date_eles:
                        show_date = show_date_eles[0].text.strip()
                        show_date = str(show_date).split("-")[0].strip().replace(" ", "")
                    else:
                        show_date = ''
                else:
                    des_list = container.cssselect("div.c-gap-top-small")
                    if des_list:
                        show_date_eles = des_list[0].xpath('descendant::span')
                        if show_date_eles:
                            show_date = show_date_eles[0].text.strip()
                            show_date = str(show_date).split("-")[0].strip().replace(" ", "")
                        else:
                            show_date = ''
                    else:
                        show_date = ''
        except AttributeError:
            return ''
        else:
            return show_date.replace('最佳答案:', '')

    def get_snapshoot_url(self, container):
        try:
            """获取快照url"""
            xpath_rules = [
                './/div[contains(@class,"se_st_footer")]/a[contains(@class,"m")]/@href',
                './/div[@class="g"]/a[@class="m"]',
                './/a[@class="m"]/@href'
            ]
            return self.get_res_text(container, xpath_rules)
        except:
            return ''

    def get_res_text(self, container, xpath_rules):
        text = ""
        for rule in xpath_rules:
            text_list = container.xpath(rule)
            for i in text_list:
                text += i.strip()
            if text != "":
                break
        return escape_string(text)

    def get_real_url(self, baidu_url, try_count=1, timeout=5):
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

    def get_cook(self):
        """
        获取有效的cookie
        :return:
        """
        try:
            key_name = 'pc'
            for i in range(2):
                if UtilBaiduCookie().totalCookies(key_name) > 0:
                    cookie = str(UtilBaiduCookie().getLastCookies(key_name=key_name)[0], encoding="utf-8")
                    return cookie
                else:
                    print('pc no use cookie')
                    return 'BAIDUID={}:FG=1; BIDUPSID={};'.format(uuid.uuid1(), uuid.uuid4())
        except:
            return 'BAIDUID={}:FG=1; BIDUPSID={};'.format(uuid.uuid1(), uuid.uuid4())


class UtilBaiduCookie(object):
    def __init__(self):
        self.redisPool = redis.ConnectionPool(**(config.DOWNLOADER_CENTER_REDIS[pro_config.ENVIR]))
        self.redisClient = redis.StrictRedis(connection_pool=self.redisPool)
        self.pc_cookie_key = 'baidu:pc:cookies'
        self.mb_cookie_key = 'baidu:mb:cookies'

    def getCookies(self, num=0, key_name='pc'):
        '''
        [获取一个有效的cookie 正序]
        :param num:
        :param key_name:
        :return:
        '''
        # noinspection PyBroadException
        try:
            if key_name == 'pc':
                return self.redisClient.zrange(self.pc_cookie_key, 0, num)
            elif key_name == 'mb':
                return self.redisClient.zrange(self.mb_cookie_key, 0, num)
            else:
                return []
        except Exception:
            return []

    def getLastCookies(self, num=0, key_name='pc'):
        '''
         [获取最新的cooie]
        :param num:
        :param key_name:
        :return:
        '''
        # noinspection PyBroadException
        try:
            if key_name == 'pc':
                return self.redisClient.zrevrange(self.pc_cookie_key, 0, num)
            elif key_name == 'mb':
                return self.redisClient.zrevrange(self.mb_cookie_key, 0, num)
            else:
                return []
        except Exception:
            return []

    def addCookies(self, cookie, key_name='pc'):
        '''
        [添加一个值]
        :param cookie:
        :param key_name:
        :return:
        '''
        # noinspection PyBroadException
        try:
            score = int(round(time.time() * 1000))
            if key_name == 'pc':
                return self.redisClient.zadd(self.pc_cookie_key, {cookie: score})
            elif key_name == 'mb':
                return self.redisClient.zadd(self.mb_cookie_key, {cookie: score})
            else:
                return 0
        except Exception:
            return 0

    def delCookies(self, cookie, key_name='pc'):
        '''
        删除cookie
        :param cookie:
        :return:
        '''
        # noinspection PyBroadException
        try:
            if key_name == 'pc':
                return self.redisClient.zrem(self.pc_cookie_key, cookie)
            elif key_name == 'mb':
                return self.redisClient.zrem(self.mb_cookie_key, cookie)
            else:
                return 0
        except Exception:
            return 0

    def totalCookies(self, key_name='pc'):
        '''
        [统计个数]
        :return:
        '''
        # noinspection PyBroadException
        try:
            if key_name == 'pc':
                return self.redisClient.zcard(self.pc_cookie_key)
            elif key_name == 'mb':
                return self.redisClient.zcard(self.mb_cookie_key)
            else:
                return 0
        except Exception:
            return 0


def remove_special_characters(text):
    text = text.replace("<b>", "")
    text = text.replace("</b>", "")
    text = text.replace("&nbsp", "")
    text = text.replace("›", "/")
    text = text.replace("...", "")
    text = text.replace(" ", "")
    return text
