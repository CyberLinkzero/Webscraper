#!/usr/bin/env python3
from argparse import ArgumentParser

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders import BenchmarkSpider

if __name__ == "__main__":
    argument_parser = ArgumentParser()
    process = CrawlerProcess(get_project_settings())
    process.crawl(BenchmarkSpider)
    process.start()
