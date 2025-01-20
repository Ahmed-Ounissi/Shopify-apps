# Scrapy settings for shopify_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "shopify_scraper"

SPIDER_MODULES = ["shopify_scraper.spiders"]
NEWSPIDER_MODULE = "shopify_scraper.spiders"
LOG_LEVEL = 'DEBUG'

ZYTE_API_KEY = 'eae5bc7df0f44971ae38269984ef6358'  # Replace with your Zyte API key
ZYTE_PROJECT_ID = 792659  # Replace with your Zyte Project ID

SCRAPEOPS_API_KEY = '4dc4ec8a-8007-4765-9cce-30e38084e4f0'

# ScrapeOps Monitoring
EXTENSIONS = {
    'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500,
}

# ScrapeOps Proxy Management
DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapeops_scrapy.middleware.user_agent.UserAgentMiddleware': 400,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "shopify_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
    'shopify_scraper.pipelines.SupabasePipeline': 300,
}

# settings.py

# Enable the Zyte proxy middleware
DOWNLOADER_MIDDLEWARES = {
    'scrapy_crawlera.CrawleraMiddleware': 610,  # Add CrawleraMiddleware
}

# Define your Zyte API Key here
CRAWLERA_APIKEY = '1bc58a3d5e3d4cf0bceef4d56019257'  # Replace with your actual API key

# Enable retry middleware (recommended for Zyte)
RETRY_TIMES = 5  # Number of retries before giving up
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]  # Retry these HTTP error codes

# Set the user-agent string (optional but recommended)
USER_AGENT = 'Mozilla/5.0 (compatible; YourBot/1.0; +http://www.yourdomain.com)'

# Configure the download delay (optional, Zyte can handle this automatically)
DOWNLOAD_DELAY = 5  # You can adjust this based on your needs

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "shopify_scraper.middlewares.ShopifyScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "shopify_scraper.middlewares.ShopifyScraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "shopify_scraper.pipelines.ShopifyScraperPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
