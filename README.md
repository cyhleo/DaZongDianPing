# DaZongDianPing
此项目用来厦门美食商铺信息，其中包含店名、人均消费、所属菜系、所属商圈、详细地址、口味评分、环境评分、服务评分信息。
# 部分结果展示
![](https://github.com/cyhleo/DaZongDianPing/blob/master/mongodbResult.png)

# 项目说明：
1. 使用scrapy框架来编写爬虫程序

2. 编写下载器中间件ProxyDownloaderMiddleware类，接入讯代理动态转发接口，实现ip切换。
在setting中设置讯代理动态转发SECRET值和ORDERNO值。

3. 编写下载器中间件UserAgentDownloaderMiddleware类，使用fake_useragent库来随机获取User-Agent。

4. 编写下载器中间件BrowserCookiesDownloaderMiddleware类，使用browsercookie库来获取浏览器中已保存的cookie信息，携带cookie进行访问。

5. 在settings中编写DEFAULT_REQUEST_HEADERS列表，构造包含Host、Accept-Encoding等信息的请求头。

6. 编写扩展Latencies类，实现每隔5秒测试一次吞吐量和响应延迟及处理延迟，
在settings中设置LATENCIES_INTERVAL值（测试间隔时间）。

7. 编写扩展SendEmail类，实现在爬虫结束时，向邮箱发送爬虫停止的原因，以及StatsCollector中存储的信息。
在settings中设置CLOSE_SPIDER_EMAIL_ENABLE值为True，设置MAIL_FROM值（邮件的发送者），
设置MAIL_HOST值（发送邮件的服务器），设置MAIL_USER值（邮箱用户名），设置MAIL_PASS值（发送邮箱的授权码），
设置MAIL_PORT值（端口号）。

8. 启用自动限速扩展，根据所爬网站的负载自动限制爬取速度。
在seting中设置AUTOTHROTTLE_ENABLED值为True，设置AUTOTHROTTLE_START_DELAY（初始的下再延迟），
设置AUTOTHROTTLE_MAX_DELAY（最大下载延迟），AUTOTHROTTLE_TARGET_CONCURRENCY（发送到服务器的请求并发量）。


9. 在settings中设置RETRY_ENABLED值为True（启用下载器中间件RetryMiddleware），RETRY_HTTP_CODES=[500, 502, 503, 504, 522, 524, 408, 302]
一旦出现302跳转至验证页面，更换ip重新请求。


10. 使用scrapy_redis内置调度器类和请求去重类，使用redis集合作为消息队列数据结构，使用redis列表作为请求指纹存储的数据结构。
在settings中设置SCHEDULER = 'scrapy_redis.scheduler.Scheduler'，DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'，
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'

11. 使用正则和xpath解析库解析HTML内容，将非结构数据转化为结构化数据。

12. 下载目标网页多个字体woff文件，对下载的信息进行字体解析。

13. 编写pipeline MongoPipeline类，将下载的数据保存至MongoDB数据库。
在settings中设置MONGO_URI值（mongodb的uri），设置MONGO_DB值（数据库名），设置MONG_COLLECTION值（集合名）
在settings中设置REDIS_HOST、REDIS_PORT、REDIS_PASSWORD值（请求队列和去重指纹队列存储使用的redis数据库info）。

# 运行项目方法
执行 dazongdianping\run.py 文件


