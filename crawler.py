import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class HTMLCrawler(scrapy.Spider):
    name = "html_crawler"
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        # Check if 'text/html' is in the Content-Type header
        content_type = response.headers.get("Content-Type", b"").decode("utf-8").lower()
        
        if "text/html" not in content_type:
            self.log(f"Skipping non-HTML page: {response.url} ({content_type})")
            return
        else:
            self.log(f"Visited: {response.url}")

        self.log(f"Crawling HTML page: {response.url}")

        # Continue following links
        for a in response.css("a"):
            yield response.follow(a, callback=self.parse)
