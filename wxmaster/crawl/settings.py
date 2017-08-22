# -*- coding: utf-8 -*-

BOT_NAME = 'wx_spider'

SPIDER_MODULES = ['wxmaster.crawl.spiders']
NEWSPIDER_MODULE = 'wxmaster.crawl.spiders'

ROBOTSTXT_OBEY = False

USER_AGENT_POOL = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2725.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2725.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
]
DOWNLOADER_MIDDLEWARES = {
    'wxmaster.crawl.middlewares.useragent.UserAgentMiddleware': 501,
    # 'wxmaster.crawl.middlewares.httpproxy.HttpProxyMiddleware': 502,
    # 'wxmaster.crawl.middlewares.httpproxy.HttpProxyWallMiddleware': 502,

    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware.': None,
}

USE_HTTPS_PROXIES = False

# 使用延迟
# DOWNLOAD_DELAY = 2
# RANDOM_DOWNLOAD_DELAY = True

# SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
# DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
# REDIS_URL = 'redis://:nlpturing2016@192.168.10.33:6381/15'
# SCHEDULER_PERSIST = False