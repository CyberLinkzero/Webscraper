import logging

from time import time

from twisted.internet import task

from scrapy.exceptions import NotConfigured
from scrapy import signals

logger = logging.getLogger(__name__)


class LogStats(object):
    """Log basic scraping stats periodically"""

    def __init__(self, stats, interval=60.0):
        self.stats = stats
        self.interval = interval
        self.multiplier = 1 / self.interval
        self.task = None

    @classmethod
    def from_crawler(cls, crawler):
        interval = crawler.settings.getfloat('LOGSTATS_INTERVAL')
        if not interval:
            raise NotConfigured
        o = cls(crawler.stats, interval)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        self.pagesprev = 0
        self.request_bytes_prev = 0
        self.response_bytes_prev = 0
        self.timeprev = None

        self.time_started = time()

        self.task = task.LoopingCall(self.log, spider)
        self.task.start(self.interval)

    def log(self, spider):
        pages = self.stats.get_value('response_received_count', 0)
        request_bytes = self.stats.get_value('downloader/request_bytes', 0)
        response_bytes = self.stats.get_value('downloader/response_bytes', 0)

        now = time()
        divider = now - self.time_started

        if self.timeprev is not None:
            self.multiplier = 1 / (now - self.timeprev)

        current_prate = (pages - self.pagesprev) * self.multiplier
        current_upload_rate = (request_bytes - self.request_bytes_prev) * self.multiplier
        current_download_rate = (response_bytes - self.response_bytes_prev) * self.multiplier

        mean_prate = pages / divider
        mean_upload_rate = request_bytes / divider
        mean_download_rate = response_bytes / divider

        self.pagesprev = pages
        self.request_bytes_prev = request_bytes
        self.response_bytes_prev = response_bytes
        self.timeprev = now

        logger.info('\n')
        logger.info('Crawled {:.2f} pages, uploaded {:.2f} bytes, received {:.2f} bytes.'.format(
            pages, request_bytes, response_bytes
        ))
        logger.info(
            'Current crawl rate: {:.2f} pages/sec. Current upload rate: {:.2f} bytes/sec. Current download rate: {:.2f} bytes/sec'.format(
                current_prate, current_upload_rate, current_download_rate
            )
        )
        logger.info(
            'Average crawl rate: {:.2f} pages/sec. Average upload rate: {:.2f} bytes/sec. Average download rate: {:.2f} bytes/sec'.format(
                mean_prate, mean_upload_rate, mean_download_rate
            )
        )

    def spider_closed(self, spider, reason):
        if self.task and self.task.running:
            self.task.stop()
