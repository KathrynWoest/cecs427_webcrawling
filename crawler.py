import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
import networkx as nx
from tqdm import tqdm

class GraphSpider(scrapy.Spider):
    name = "graph_spider"

    def __init__(self, max_nodes, domain_filter, start_urls, *args, **kwargs):
        super(GraphSpider, self).__init__(*args, **kwargs)
        self.max_nodes = int(max_nodes)
        self.domain_filter = domain_filter.strip()       
        self.start_urls = start_urls
        self.count = 0
        self.found_edges = []
        self.G = nx.DiGraph() # Initialize a NetworkX Directed Graph

        # Initialize the progress bar
        self.pbar = tqdm(total=self.max_nodes, desc="Crawling Pages", unit="pg")

    def parse(self, response):
        # Check if 'text/html' is in the Content-Type header
        content_type = response.headers.get("Content-Type", b"").decode().lower()

        if "text/html" not in content_type:
            return
        
        if self.count >= self.max_nodes:
            raise CloseSpider('reached_node_limit')

        self.count += 1
        self.pbar.update(1) # Move the bar forward
        current_url = response.url
        self.G.add_node(current_url) # Add the current page as a node

        # List of extensions to ignore
        forbidden_extensions = (
            '.ris', '.xml', '.bib', '.pdf', 
            '.rdf', '.rss', '.ttl', '.dn'
        )

        for a in response.css("a"):
            # Check if 'href' exists before doing anything else
            href = a.attrib.get('href')
            if not href:
                continue

            link = response.urljoin(href).split('?')[0].split('#')[0] # Strip queries/anchors
     
            # the link should be in the same domain, must not end with a forbidden extension,
            # and must not be a self-loop
            if (link.startswith(self.domain_filter) and 
                not link.lower().endswith(forbidden_extensions) and 
                link != current_url):
                
                self.G.add_edge(current_url, link)
                yield response.follow(a, callback=self.parse)

    def closed(self, reason):
        self.pbar.close() # Clean up the bar

        # Ensuring exactly 100 nodes in the GML
        if len(self.G.nodes) > self.max_nodes:
            nodes_to_keep = list(self.G.nodes)[:self.max_nodes]
            self.G = self.G.subgraph(nodes_to_keep).copy()

        # Saving gml graph
        nx.write_gml(self.G, "out_graph.gml")
        print("Successfully saved graph to out_graph.gml")

# File reading logic for the input text file
def run_from_file(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Parsing file into the correct format
    # Line 1: Limit | Line 2: Filter | Line 3+: Seed URLs
    max_nodes = lines[0]
    domain_filter = lines[1]
    seeds = lines[2:]

    # Set up to mimic the behavior of a browser to bypass DBLP anti-crawling measures
    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'INFO',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'ROBOTSTXT_OBEY': True,

        'DEPTH_PRIORITY': 1,
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
        
        'DOWNLOAD_DELAY': 2.0,              # Wait 2 seconds between every page
        'RANDOMIZE_DOWNLOAD_DELAY': True,   # Add a random variation (0.5x to 1.5x of delay)
        'CONCURRENT_REQUESTS': 1,           # Only download 1 page at a time
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_TIMES': 5,                   # If it fails, try a few more times
        'RETRY_HTTP_CODES': [429, 500, 502, 503, 504],
    })
    process.crawl(GraphSpider, max_nodes=max_nodes, domain_filter=domain_filter, start_urls=seeds)
    process.start()

if __name__ == "__main__":
    run_from_file('crawlingFile.txt')