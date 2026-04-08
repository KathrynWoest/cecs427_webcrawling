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

    # initialize round 0, where the page rank of each node is the initial page rank calculated above
    nx.set_node_attributes(graph, initial_pr, name="page_rank")
    newpr_graph = copy.deepcopy(graph)

    # loop through the algorithm for the rest of the rounds
    for i in range(100):
        # create a copy of the graph from the previous round to use for page rank distribution, and then reset the current graph
        last_step_graph = copy.deepcopy(newpr_graph)
        nx.set_node_attributes(newpr_graph, 0, name="page_rank")

        # for every node in the graph
        for node, rank in last_step_graph.nodes(data="page_rank"):
            # calculate all of the out-edges
            edges = list(last_step_graph.out_edges(node))
            # if the node has out-edges, calculate the amount of page rank to distribute to each outgoing node
            if edges:
                shared_pr = rank/len(edges)
                for _, v in edges:
                    # distribute the outgoing page rank to each node
                    newpr_graph.nodes[v]["page_rank"] = newpr_graph.nodes[v].get("page_rank", 0) + shared_pr
            # otherwise, let the current node keep all of its current rank
            else:
                newpr_graph.nodes[node]["page_rank"] = rank
        
        # TODO: some sort of check here if it's been a certain number of loops
        #       if yes, then call `distribute()`

    # store the results in the given output file
    store_pr(newpr_graph, output_file)
