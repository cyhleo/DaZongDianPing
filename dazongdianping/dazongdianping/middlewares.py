# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
from fake_useragent import UserAgent
import time
import hashlib
import browsercookie
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from scrapy.http import HtmlResponse
from twisted.internet import defer
from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.web.client import ResponseFailed

logger = logging.getLogger(__name__)

class DazongdianpingSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DazongdianpingDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class UserAgentDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.



    def process_request(self, request, spider):
        agent = UserAgent()
        agent_one = agent.random
        logger.debug("user_agent:{}".format(agent_one))
        request.headers['User-Agent'] = agent_one


class ProxyDownloaderMiddleware(object):
    def __init__(self, secret, orderno):
        self.secret = secret
        self.orderno = orderno

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            secret=crawler.settings.get('SECRET'),
            orderno=crawler.settings.get('ORDERNO')
        )

    def process_request(self, request, spider):
        timestamp = str(int(time.time()))
        string = "orderno=" + self.orderno + "," + "secret=" + self.secret + "," + "timestamp=" + timestamp
        string = string.encode()
        md5_string = hashlib.md5(string).hexdigest()
        sign = md5_string.upper()
        auth = "sign=" + sign + "&" + "orderno=" + self.orderno + "&" + "timestamp=" + timestamp

        request.meta['proxy'] = 'http://forward.xdaili.cn:80'
        request.headers["Proxy-Authorization"] = auth
        logger.debug('正在使用动态转发')

class BrowserCookiesDownloaderMiddleware(object):

    def process_request(self, request, spider):
        request.headers['cookies'] = self.cookie_dict
        logger.info('cookie_dict:{}'.format(self.cookie_dict))

    def __init__(self):
        cookiejar = browsercookie.chrome()
        self.cookie_dict = {}
        for cookie in cookiejar:
            if cookie.domain == '.dianping.com':
                self.cookie_dict[cookie.name] = cookie.value
        self.cookie_dict['navCtgScroll'] = '0'

class ExceptionDownloaderMiddleware(object):
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError, ResponseFailed,
                           IOError, TunnelError)


    def process_response(self,request,response,spider):
        if str(response.status).startswith('4') or str(response.status).startswith('5'):
            with open(str(spider.name) + ".txt", "a") as f:
                f.write('{}got a response.status:{}'.format(request.url, response.status) + "\n")
            response = HtmlResponse(url='')
            logger.debug('{}got a response.status:{}'.format(request.url, response.status))
            return response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception,self.ALL_EXCEPTIONS):

            with open(str(spider.name) + ".txt", "a") as f:
                f.write('{}got a exception:{}'.format(request.url,exception) + "\n")
            logger.debug('{}got a exception:{}'.format(request.url, exception))
            response = HtmlResponse(url='')
            return response

        logger.debug('{}got a exception:{},but not return response obj'.format(request.url, exception))