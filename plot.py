import json
import networkx as nx
import matplotlib.pyplot as plt

def plot(gml_file, output_image="web_graph.png"):

    try:
        # Load the graph
        G = gml_file
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
    
    plt.title("URL Discovery Directed Graph")

    # Saving the figure
    plt.savefig(output_image, format="png", dpi=300, bbox_inches="tight")
    print(f"Graph successfully saved as {output_image}")

    print("Opening graph window...")
    plt.show()

# if __name__ == "__main__":
#     plot('out_graph.gml')