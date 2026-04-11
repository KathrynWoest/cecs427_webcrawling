import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
import networkx as nx
from tqdm import tqdm

class GraphSpider(scrapy.Spider):
    """
    A Scrapy spider that crawls web pages within a specified domain and
    constructs a directed graph of page links using NetworkX.
    """

    name = "graph_spider"

    def __init__(self, max_nodes, domain_filter, start_urls, *args, **kwargs):
        """
        Initializes the spider with a node limit, domain filter, and seed URLs.

        Inputs:
            max_nodes (int): Maximum number of pages (nodes) to crawl.
            domain_filter (str): Domain prefix to restrict crawling.
            start_urls (list): List of initial seed URLs.
        """

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
        """
        Parses a downloaded page, extracts valid HTML links within the domain,
        and adds edges to the graph. Also schedules new pages to crawl.

        Input:
            response (scrapy.http.Response): The HTTP response of the current page.
        """

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

        for a in response.css("a"):
            # Check if 'href' exists before doing anything else
            href = a.attrib.get('href')
            if not href:
                continue

            link = response.urljoin(href).split('?')[0].split('#')[0] # Strip queries/anchors

            if not link.endswith(".html"):
                continue
     
            # the link should be in the same domain and must not be a self-loop
            if (link.startswith(self.domain_filter) and link != current_url):
                
                self.G.add_edge(current_url, link)
                yield response.follow(a, callback=self.parse)

    def closed(self, reason):
        """
        Finalizes the crawl by saving the constructed graph to a GML file.

        Input: 
            reason (str): Reason why the spider was closed.
        """

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
    """
    Reads crawling parameters from a file and starts the spider.

    The format of the input file should be:
    - Line 1: Maximum number of nodes
    - Line 2: Domain filter (URL)
    - Remaining lines: Seed URLs

    Input:
        filename (str): Path to the input configuration file.
    """

    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Parsing file into the correct format
    # Line 1: Limit | Line 2: Filter | Line 3+: Seed URLs
    max_nodes = lines[0]
    domain_filter = lines[1]
    seeds = lines[2:]

    # Set up to mimic the behavior of a browser to bypass anti-crawling measures
    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'INFO',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'ROBOTSTXT_OBEY': True,

        'DEPTH_PRIORITY': 1,
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
        
        'DOWNLOAD_DELAY': 2.0,              
        'RANDOMIZE_DOWNLOAD_DELAY': True,   
        'CONCURRENT_REQUESTS': 1,           
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_TIMES': 5,                   
        'RETRY_HTTP_CODES': [429, 500, 502, 503, 504],
    })
    process.crawl(GraphSpider, max_nodes=max_nodes, domain_filter=domain_filter, start_urls=seeds)
    process.start()

# if __name__ == "__main__":
#     run_from_file('crawlingFile.txt')