## NOTE: this file reuses a lot of code from Projects 1-4

import sys
import file_io as fio
#import crawl
#import plot
import pagerank as pr


def main():
    # get arguments from command line
    args = sys.argv
    end = len(args)

    if end < 3:
        raise Exception(f"Program was terminated because there are not enough arguments to upload or generate a graph. Minimum required arguments: 3. Arguments provided: {end}.")
    
    # parse or generate graph
    else:
        # parse in graph from given .gml file
        if "--crawler" in args:
            crawl_info = args[args.index("--crawler") + 1]  # TODO: crawl needs to check that the provided file is a .txt file
            #user_graph = crawl.crawl(crawl_info)
        elif "--input" in args:
            input_file = args[args.index("--input") + 1]
            user_graph = fio.parse_graph(input_file)
        # generate graph with given .txt file, override --input graph
        # if there are 3 arguments and we aren't inputting a file, then not enough arguments to generate graph. terminate program.
        else:
            raise Exception("Program was terminated because it was missing '--input' or '--crawler' arguments and/or their input files.")

    # call the plotting function
    #if "--loglogplot" in args:
        #plot.plot(user_graph)

    # call the saving graph function
    if "--crawler_graph" in args:
        if args.index("--crawler_graph") + 1 == end:
            print("Saving the graph failed because it was missing the output file name.")
        
        else:
            output_file = args[args.index("--crawler_graph") + 1]
            fio.save_graph(user_graph, output_file)

    # call the pagerank values function
    if "--pagerank_values" in args:
        if args.index("--pagerank_values") + 1 == end:
            print("Calculating pagerank failed because it was missing the output file name.")
        
        else:
            output_file = args[args.index("--pagerank_values") + 1]
            pr.calculate(user_graph, output_file)

main()