from pyrgg import __main__ # need to install pyrgg first: pip install pyrgg==0.9     #input randomgraph as filename, 10 as graph format, 2 for unweighted, 2 for undirected, 1 for simple, any for self loop, 2 for unsigned, any edge and vertice number
#creates a tsv file to your current working directory (address printed as output), and returns the dictionary of node keys as well
def generateRandomGraph(self, readGraph):
    __main__.run()
    randomGraph  =  readGraph(os.getcwd()+"\\randomgraph.tsv")
    return randomGraph