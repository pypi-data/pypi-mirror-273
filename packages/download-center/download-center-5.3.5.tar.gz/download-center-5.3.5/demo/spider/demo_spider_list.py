# -*- coding: utf-8 -*-
import hashlib
import json
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

from scrapy.http.cookies     import CookieJar

from download_center.new_spider.downloader.downloader import SpiderRequest
from download_center.new_spider.spider.basespider import BaseSpider
from download_center.new_spider.util.util_baidu_relate import UtilBaiduRelate
from download_center.util.util_log import UtilLogger

# 线上测试
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print("PROJECT_PATH", PROJECT_PATH)
sys.path.append(PROJECT_PATH)
# sys.path.append(os.path.join(PROJECT_PATH, 'demo'))
# from demo.extractor.baidu_extractor import BaiduExtractor
# from extractor.baidu_extractor import BaiduExtractor


class DemoSpider(BaseSpider):
    def __init__(self, remote=True):
        super(DemoSpider, self).__init__(remote=remote)
        self.log = UtilLogger('DemoSpider', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_demo_spider'))
        # self.ext = BaiduExtractor()
        # self.downloader.reset_ip()

    def get_user_password(self):
        return 'test', 'Welcome#1'

    # def tn(self):
    #     return random.choice(
    #         ['baiduhome_pg'])
        # return random.choice(
        #     ['50000021_hao_pg', 'site888_3_pg', '77021190_cpr', 'site5566', '520com_pg', '51010079_cpr'])

    def start_requests(self):
        try:
           for i in range(100):
               urls = [{
                   'url': 'https://www.baidu.com/s?%s' % (urllib.parse.urlencode({'word': '联想','pn':10})),
                   # 'type': 1,
                   'type': 17,
                   'unique_key':self.get_unique_key()#默认md5 url 字段，不写则表示相同链接只查一次
               }]
               config={"param": {'cu':'https://www.baidu.com','et':0},"conf_district_id":0}
               untilBaidu = UtilBaiduRelate()
               # headers = untilBaidu.getBaiduMbHeader()
               headers = untilBaidu.getBaiduPcHeader()
               request = SpiderRequest(headers=headers, urls=urls,config=config)
               self.sending_queue.put(request)
               time.sleep(0.1)

        except Exception:
            self.log.error('获取初始请求出错: {}'.format(traceback.format_exc()))

    def get_stores(self):
        # 存储器
        stores = list()
        return stores

    def deal_response_results_status(self, task_status, url, result, request):
        """
        Args:
            task_status:
            url:
            result:
            request:

        Returns:
        根据自己的解析类型做不同的处理，默认返回html
        """
        if task_status == '2':
            config = request.config
            try:
                self.store_queue.put(result["result"])
                # result = json.loads(result["result"])
                if result["code"] not in [0,200]:#老版下载中心是0,新版下载中心是 200
                    print("结果获取错误。code:{}".format(result["code"]))
                    return
                if '百度安全验证' in result["result"]:
                    print("结果抓取失败，百度安全验证")
                else :
                    print("成功!，长度：{},url：{}".format(len(result), url['url']))
            except Exception as e:
                print('失败！url：{}'.format( url['url']))

            # rdata = self.ext.ext ractor(result["result"])
            # self.store_queue.put(result)
            # if isinstance(rdata, int):
            #     print("request ua: {}".format(request.headers["User-Agent"]))
            # else:
            #     result_d, include, keyword_list = rdata
            #     print(result_d)
            #     print(include)
            #     print(keyword_list)
            #
            # with open("html_py3_3.txt", 'w', encoding="utf-8") as f:
            #     f.write(result["result"])
        else:
            self.log.info('抓取失败: {}'.format(url))

    def to_store_results(self,  results, stores):
        """
        结果存储按需使用
        :return:
        """
        pass


def main():
    # spider = DemoSpider(remote=False)
    spider = DemoSpider(remote=True)
    spider.run(1, 1, 1, 1, record_log=True)   # 测试
    # spider.run(spider_count=1000, record_log=True)
    # spider.run(record_log=True)               # error



if __name__ == '__main__':
    main()
