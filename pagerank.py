import networkx as nx
import copy


def store_pr(graph, output_file):
    """Function that saves the pagerank results into a .txt file
    Inputs: the graph with all the page ranks saved to the nodes and a .txt file name to save them in
    Outputs: N/A"""

    try:
        with open(output_file, "w") as f:
            for node, rank in graph.nodes(data="page_rank"):
                f.write(f"Node {node}: {rank}\n")
    except Exception as e:
        print(f"Something went wrong with the saving of the page rank results. Error:", e)
        return


def distribute(graph):
    """Function that redistributes the page rank by a factor of c to prevent it from pooling in dead-ends
    Input: the graph with all the page ranks saved to the nodes
    Output: the graph with the redistributed page ranks"""

    pass


def calculate(graph, output_file):
    """Function that calculates the page ranks of the given graph
    Inputs: the graph to find the page ranks of and a .txt file to save the results
    Outputs: N/A"""

    if ".txt" not in output_file:
        print("Output file name type is not .txt, so calculating page rank terminated. Provided file:", output_file)
        return
    
    # calculate the initial page rank for every node
    num_nodes = len(graph.nodes())
    initial_pr = 1/num_nodes

    # create a copy of the graph to track changes and assign each node with the initial page rank
    nx.set_node_attributes(graph, 0, name="page_rank")
    newpr_graph = copy.deepcopy(graph)
    nx.set_node_attributes(graph, initial_pr, name="page_rank")

    for node, rank in graph.nodes(data="page_rank"):
        edges = list(graph.out_edges(node))
        if edges:
            shared_pr = rank/len(edges)
            for u, v in edges:
                newpr_graph.nodes[v]["page_rank"] = newpr_graph.nodes[v].get("page_rank", 0) + shared_pr
        else:
            newpr_graph.nodes[node]["page_rank"] = rank

    store_pr(newpr_graph, output_file)
