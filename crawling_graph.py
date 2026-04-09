import json
import networkx as nx
import matplotlib.pyplot as plt

def plot(json_file):
    G = nx.DiGraph()
    
    try:
        with open(json_file, 'r') as f:
            edges = json.load(f)
    except FileNotFoundError:
        print("No output.json found. Run the crawler first.")
        return

    for edge in edges:
        G.add_edge(edge['source'], edge['target'])

    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, k=0.5)  # spring layout for easier viewing
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightgreen", 
            font_size=7, arrows=True)
    plt.title("Web Discovery Directed Graph")
    plt.show()
