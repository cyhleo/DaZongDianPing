from scrapy import signals
class MyExtend(object):
    def __init__(self,crawler):
        # 在指定信号signals.engine_started注册self.start函数
        # 在爬虫开始的时候执行self.start函数
        crawler.signals.connect(self.start,signals.engine_started)
    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def start(self):
        print('在引擎开始的时候执行')