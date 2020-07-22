LOG_LEVEL = 'INFO'
HTTPERROR_ALLOW_ALL = True
DOWNLOADER_STATS = True

CONCURRENT_REQUESTS = 2 ** 32

EXTENSIONS = {
    'scrapy.extensions.logstats.LogStats': None,
    'logstats.LogStats': 0
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': None,
    'downloadermiddlewares.httpcompression.FixedHttpCompressionMiddleware': 590,
}

from conf import *

RANDOMIZE_DOWNLOAD_DELAY = False
DOWNLOAD_DELAY = 1 / PAGES_PER_DOMAIN_PER_SECOND
CONCURRENT_REQUESTS_PER_IP = PAGES_PER_DOMAIN_PER_SECOND
