from twisted.internet import task
import time
from scrapy import signals
from scrapy.exceptions import NotConfigured

class Latencies(object):
    # 每隔LATENCIES_INTERVAL秒记录一次吞吐量、平均延迟和item经过pipeline的延迟
    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def __init__(self,crawler):
        self.crawler = crawler
        self.latency,self.items,self.proc_latency = 0,0,0
        crawler.signals.connect(self._spider_opened, signals.spider_opened)
        crawler.signals.connect(self._spider_closed, signals.spider_closed)
        crawler.signals.connect(self._response_received, signals.response_received)
        crawler.signals.connect(self._item_scraped, signals.item_scraped)
        # signals.request_scheduled:当一个引擎从调度器取走一个request对象的时候触发
        crawler.signals.connect(self._request_scheduled,signals.request_scheduled)
        self.interval = crawler.settings.getint('LATENCIES_INTERVAL')
        if not self.interval:
            raise NotConfigured

    def _spider_opened(self,spider):
        self.task = task.LoopingCall(self._log, spider)
        # 爬虫开始后self.interval秒后开始执行self._log方法
        self.task.start(self.interval)


    def _spider_closed(self):
        if self.task and self.task.running:
            self.task.stop()

    def _request_scheduled(self,spider,request):
        # schedule_time：记录爬虫开始的时间
        request.meta['schedule_time'] = time.time()

    def _response_received(self,spider,request,response):
        # response_time：记录引擎从downloader获取response对象的时间
        response.meta['response_time']= time.time()
    def _item_scraped(self,spider,response,item):
        # self.latency：记录从调度器取走请求对象到item被数据库存储所用的时间
        self.latency += time.time() - response.meta['schedule_time']
        # self.proc_latency：记录响应经过爬虫中间件、spider、item pipeline所用的时间
        self.proc_latency += time.time() - response.meta['response_time']
        # 当有一个item被存储时，self.items数量加一
        self.items += 1
    def _log(self,spider):
        # irate：记录self.interval秒内的平均每秒爬多少的item。
        irate = self.items / self.interval
        # latency：记录self.interval秒内平均每个item从调度器提出请求到item被数据库保存，所用的时间
        latency = self.latency /self.items if self.items else 0
        # proc_latency：记录self.interval秒内每个item响应经过爬虫中间件、spider、item pipeline所用的时间
        proc_latency = self.proc_latency /self.items if self.items else 0

        msg = ("Crawled %d items at %0.2f items/s, avg latency:%0.2f s,avg time in pipelins:%0.2f s"
               %(self.items,irate,latency,proc_latency))
        log_args = {'items': self.items, 'itemrate': irate,
                    'latency': latency, 'proc_latency': proc_latency}

        # 将爬取的信息放到日志中
        spider.logger.info(msg)
        self.latency, self.items, self.proc_latency = 0, 0, 0

