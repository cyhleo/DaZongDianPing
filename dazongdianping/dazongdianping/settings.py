# -*- coding: utf-8 -*-

# Scrapy settings for dazongdianping project
#


BOT_NAME = 'dazongdianping'

SPIDER_MODULES = ['dazongdianping.spiders']
NEWSPIDER_MODULE = 'dazongdianping.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# 设置最小的下载延迟时间
DOWNLOAD_DELAY = 0.1

# 设置并发数
CONCURRENT_REQUESTS = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 2
CONCURRENT_REQUESTS_PER_IP = 2


# 设置请求头
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
  'Accept-Encoding':'gzip, deflate',
  'Cache-Control':'max-age=0',
  'Connection':'keep-alive',
  'Host':'www.dianping.com',
  'Upgrade-Insecure-Requests':1,
  'Accept-Language': 'zh-CN,zh;q=0.9',
}


# 下载器中间件设置
DOWNLOADER_MIDDLEWARES = {
   'dazongdianping.middlewares.UserAgentDownloaderMiddleware': 543,
   'dazongdianping.middlewares.ProxyDownloaderMiddleware': 545,
   'dazongdianping.middlewares.BrowserCookiesDownloaderMiddleware': 600,
   'dazongdianping.middlewares.ExceptionDownloaderMiddleware': 100,
}


# 扩展设置
EXTENSIONS = {
    'dazongdianping.latencies.Latencies': 500,
    'dazongdianping.close_email.SendEmail': 500
}

# 设置设置吞吐量和延迟的时间间隔
LATENCIES_INTERVAL = 5

CLOSE_SPIDER_EMAIL_ENABLE = False
# 邮件发送者
MAIL_FROM = ''
# 发送邮件的服务器
MAIL_HOST = ''
# 邮箱用户名
MAIL_USER = ''
# 发送邮箱的授权码
MAIL_PASS = ''
MAIL_PORT = 465
MAIL_TLS=True
MAIL_SSL=True


LOG_ENABLED = True
LOG_ENCODING = 'utf-8'

#logger输出格式设置
LOG_FORMATTER = 'scrapy.logformatter.LogFormatter'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# 如果为True，则进程的所有标准输出（和错误）将重定向到日志。 例如，如果您打印（'hello'）它将出现在Scrapy日志中。
LOG_STDOUT = True

# 显示的日志最低级别
LOG_LEVEL = 'INFO'

import datetime
t = datetime.datetime.now()
log_file_path = './log_{}_{}_{}.log'.format(t.month,t.day,t.hour)
# log磁盘保存地址
LOG_FILE = log_file_path


# 开启自动限速设置
AUTOTHROTTLE_ENABLED = True

# The initial download delay
AUTOTHROTTLE_START_DELAY = 5

# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60

# 发送到每一个服务器的并发请求数量
AUTOTHROTTLE_TARGET_CONCURRENCY = 2


# 是否开启调试模式，将显示收到的每个响应的统计信息，
# 以便观察到延迟发送请求的时间如何一步步被调整
AUTOTHROTTLE_DEBUG = False


# ITEM_PIPELINES设置
ITEM_PIPELINES = {
   'dazongdianping.pipelines.MongoPipeline': 300,
}

MONGO_URI = ''
MONGO_DB = ''
MONG_COLLECTION = ''

# 在爬虫结束的时候不清空请求队列和去重指纹队列
SCHEDULER_PERSIST = True
# 在爬虫开始的时候不清空请求队列
SCHEDULER_FLUSH_ON_START = False

# 启用scrapy_redis内置的调度器
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
# 启动scrapy_redis内置的请求去重类
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
# 启用scrapy_redis内置的先进先出队列
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'

#请求队列和去重指纹队列存储使用的redis数据库info
REDIS_HOST = ''
REDIS_PORT = ''
REDIS_PASSWORD = ''

# 布尔值，指定是否 启用telnet控制台（
TELNETCONSOLE_ENABLED = True
# 用于telnet控制台的端口范围。如果设置为None或0，则使用动态分配的端口。
TELNETCONSOLE_PORT = [6023, 6073]
TELNETCONSOLE_HOST = '127.0.0.1'
# telnet连接认证的用户名
TELNETCONSOLE_USERNAME = 'scrapy'
# telnet连接认证的密码
TELNETCONSOLE_PASSWORD = ''

# 动态转发设置
SECRET = ''
ORDERNO = ''

RETRY_ENABLED = True
# 最大重试次数
RETRY_TIMES = 6  # initial response + 6 retries = 7 requests
# 需要重试的响应重试状态码
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 302]

# 关闭重定向中间件
REDIRECT_ENABLED = False