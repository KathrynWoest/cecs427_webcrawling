# CECS 427 Project 5: Information Network and the WWW
Completed By: Kathryn Woest (030131541) and Grace Flores (030169163)


## Usage Instructions

1. Clone this repo and open it on your IDE

2. DEPENDENCIES: This program relies on five external libraries. To install them, ensure you are inside the project directory and run these commands:
    1. **NetworkX**, a library that provides `.gml` file parsing and writing, graph support, and analysis functions. To install, run: `pip install networkx[default]`
    2. **pathlib**, a built-in library for handling file and directory paths.
    3. **Scrapy**, a library used for page crawling and scraping. To install, run `pip install scrapy`
    4. **tqdm**, a library used for creating progress bars. To install, run `pip install tqdm`
    5. **matplotlib**, a library used for creating and plotting graphs. To install, run `pip install matplotlib`

3. Run this program with: `python page_rank.py --crawler crawler.txt --input input_graph.gml --loglogplot --crawler_graph out_graph.gml --pagerank_values node_rank.txt`
    1. `--crawler` is the default argument to produce the graph, and will override `--input` if both exist in the arguments. However, one of them is required in order for the program to function.
    2. The `--` arguments may be provided in any order. However, if the argument is followed by a parameter, like the input graph or the node rank file name, then it must have the parameter and the parameter must directly follow that argument. For example, if you want to save the crawler graph, you must have `--crawler_graph out_graph.gml` in the input, not something like `--crawler_graph --loglogplot out_graph.gml`.
    3. All arguments, other than either `--crawler` or `--input`, are optional.


## Implementation Description
1. **Overall Program:** Modular program that utilizes a given `.txt` file to crawl a subset of pages on the WWW to make a directed crawler graph. If `--crawler` is not in the inputs, then it will take `--input` to read in a directed `.gml` file to utilize instead. This graph MUST be directed, page rank is unable to be calculated on an undirected graph. Then the user can optionally choose to generate a loglog plot of the graph, save the graph to a `.gml` file, and/or calculate the graph's page rank and save that to a `.txt` file.
2. **MAIN - page_rank.py:** Reads in all of the arguments and calls desired functions and calculations based on those arguments. Conducts error checking for inputs. A lot of code is reused from projects 1-4.
3. **file_io.py:** Contains two functions. `parse_graph()` reads in the graph from the given `.gml` file, checks that the graph is not empty, ensures the graph is directed (required for page_rank to run), then returns the graph to the main program for analysis. `save_graph()` takes the user's crawled graph and saves it in the givem `.gml` file. A lot of code is reused from projects 1-4.
4. **pagerank.py:** Contains two functions. `store_pr()` takes the calculated page rank values and stores them in the given `.txt` file with the format *node label: node page rank*. `calculate()` calculates the page rank. It begins by calculating initial page rank (1/n) and distributing to each node. It saves the current graph's rank, then calculates the next step of page rank by going through each node, dividing its rank among its neighbors, and saving the sum of the incoming ranks to each node. Then 0.15 of the results are redistributed at the end of each calculation to prevent page rank from pooling in nodes that don't point to the rest of the graph. Finally, the program checks to see if the page ranks between the last step and the current step changed less than 1e-6. If they did, it indicates that the rank reached an equilibrium, and stops calculating the rank before calling `store_pr()`. If the change was greater than 1e-6, then the entire process repeats until the change is less. This ensures page rank calculation stops based on the current inputted graph, and not based on an arbitrary loop count.
5. **plot.py:** Contains two functions: `plot()` and `loglog()`. `plot()` generates a visualization of the crawl graph using `out_graph.gml`. `loglog()` generates a log-log graph of the specified graph's degree distribution.
6. **crawler.py:** Contains the `GraphSpider` class used for page crawling and `run_from_file()` which runs the crawler. `GraphSpider` contains two functions: `parse()` parses each of the crawled pages and builds the `.gml` graph; `closed()` closes the crawler and generates the output directed graph named `out_graph.gml`. `run_from_file()` takes in the name of the input file and starts the crawling process. The input file must be in this format: *Line 1: Maximum number of  (pages) | Line 2: Domain filter (URL) | Remaining lines: Seed URLs.*


## Example Commands and Outputs
1. Command: `python3 page_rank.py --crawler crawlingFile.txt --loglogplot`
2. Command: `python3 page_rank.py --input sm_graph.gml --pagerank_values node_rank.txt`
3. Command: `python3 page_rank.py --crawler crawlingFile.txt --crawler_graph out_graph.gml`

Outputs are annotated in this PDF: https://pdflink.to/24ddb647/