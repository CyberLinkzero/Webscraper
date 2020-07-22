from urllib.parse import urlparse, urlunparse, ParseResult

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request


def add_scheme(url):
    parse_result = urlparse(url)
    if not parse_result.scheme:
        url = 'http://{}'.format(url)
    return url


class BenchmarkSpider(CrawlSpider):
    name = 'benchmark'
    rules = (
        Rule(LinkExtractor()),
    )

    def start_requests(self):
        f = open(self.settings['URLS_FILE'])
        for line in f:
            yield Request(add_scheme(line))
