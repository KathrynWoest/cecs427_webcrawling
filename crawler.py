import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse

class GraphSpider(scrapy.Spider):
    name = "graph_spider"

    def __init__(self, max_nodes, domain, start_urls, *args, **kwargs):
        super(GraphSpider, self).__init__(*args, **kwargs)
        self.max_nodes = int(max_nodes)
        self.allowed_domains = [domain]
        self.start_urls = start_urls
        self.count = 0
        self.found_edges = []

    def parse(self, response):
        # Check if 'text/html' is in the Content-Type header
        content_type = response.headers.get("Content-Type", b"").decode().lower()
        if "text/html" not in content_type:
            return

        # Node limit check
        if self.count >= self.max_nodes:
            return

        self.count += 1
        current_url = response.url

        for a in response.css("a"):
            link = response.urljoin(a.attrib.get('href'))
            
            # Check if same domain
            if urlparse(link).netloc == self.allowed_domains[0]:
                self.found_edges.append({"source": current_url, "target": link})
                yield response.follow(a, callback=self.parse)

    def closed(self, reason):
        import json
        with open('output.json', 'w') as f:
            json.dump(self.found_edges, f)

# .txt file reading logic
def run_from_file(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Parsing the correct format
    max_nodes = int(lines[0])
    domain = lines[1]
    start_urls = lines[2:]

    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'INFO',
    })
    process.crawl(GraphSpider, max_nodes=max_nodes, domain=domain, start_urls=start_urls)
    process.start()
