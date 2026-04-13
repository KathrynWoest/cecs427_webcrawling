import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

def plot(gml_file, output_image="web_graph.png"):
    """
    Loads a graph from a GML file and visualizes it using NetworkX and Matplotlib.

    Inputs:
        gml_file (str): The graph to be visualized.
        output_image (str): Filename for the saved plot image. Default name is `web_graph.png`.
    """

    # Loading the graph from the given gml file
    try:
        G = nx.read_gml(gml_file)
    except Exception as e:
        print(f"Error loading GML: {e}")
        return

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42, k=0.6, iterations=1)
    nx.draw(G, pos, 
            with_labels=True, 
            node_size=50, 
            node_color='skyblue',
            edge_color='grey', 
            width=1.0,
            arrows=False,
            font_size=6)
    
    plt.title("Crawl Graph")

    # Saving the figure
    plt.savefig(output_image, format="png", dpi=300, bbox_inches="tight")
    print(f"Graph successfully saved as {output_image}")

    print("Opening graph window...")
    plt.show()

def loglog(graph):
    """
    Plots a log-log graph of the given graph's degree distribution.

    Input: 
        - graph (nx.DiGraph): The graph for which the log-log graph will be generated.
    """

    if type(graph) is None:
        raise TypeError("The graph cannot be None. Please provide a valid GML file.")

    # Calculating the degree of each node
    degree_sequence = [d for n, d in graph.degree()]

    # Counting the frequency of each degree and sorting
    degree_counts = Counter(degree_sequence)
    sorted_counts = sorted(degree_counts.items()) 
    x, y = zip(*sorted_counts)

    # Plotting the log-log graph
    plt.figure(figsize=(8, 6))
    plt.loglog(x, y, linestyle='-', color='#1f77b4')

    plt.title("LogLog Plot")
    plt.xlabel("number of nodes (log)")
    plt.ylabel("degree (log)")

    plt.grid(False) 
    plt.show()

