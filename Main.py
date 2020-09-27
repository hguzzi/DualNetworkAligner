# Package for the creation, manipulation,
# and study of the structure, dynamics,
# and functions of complex networks.
# https://networkx.github.io/
import networkx as nx

# Imports the custom functions
from DualNetworkAligner import buildGraph, pairwiseAlignment
from CharikarDCSExtractor import extractDCS

# Utility packages
from datetime import datetime


# EXAMPLE

# Folder with the name of dataset to analize
datasetNameFolder = "STRING/"  # <-- MODIFY to select dataset
# Directory path of dataset to analize
inputDirectotyPath = "Dataset/"+datasetNameFolder + "Input/"
# Directory path to store results
outputDirectoryPath = "Dataset/"+datasetNameFolder + "Output/"

t1 = datetime.now()  # used to calculate the execution time
print(t1, " --> STARTED...")
print("Dataset/"+datasetNameFolder)

# INPUT file
# Text file of weighted graph
weightedGraphFile = inputDirectotyPath+"weightedGraph.txt"
# Text file of weighted graph
unweightedGraphFile = inputDirectotyPath+"unweightedGraph.txt"
# Text file of Similarity relationship among dual networks nodes
simFile = inputDirectotyPath+"similarityFile.txt"

# OUTPUT file
# Compressed Pickle file of the weighted graph
weightedGraphPickle = outputDirectoryPath+"weightedGraph.gz2"
# Compressed Pickle file of the unweighted graph
unweightedGraphPickle = outputDirectoryPath+"unweightedGraph.gz2"
# Compressed Pickle file of the alignment graph
alignmentGraphPickle = outputDirectoryPath+"alignmentGraph.gz2"
# Compressed Pickle file of the DCS graph
dcsGraphPickle = outputDirectoryPath+"dcs.gz2"

# STEP ONE: build the graphs

# Builds the weighted graph W
print(datetime.now(), " --> build weighted graph W...")
W = buildGraph(weightedGraphFile, skipLines=0,
               splitSep=" ", weightedEdges=True)
print(datetime.now(), " --> W: nodes ",
      len(W.nodes()), " edges: ", len(W.edges()))

# Stores the weighted graph in a pickle file
# nx.write_gpickle(W, weightedGraphPickle) # UNCOMMENT this line if you want to save a graph

# Builds the unweighted graph U
print(datetime.now(), " --> build unweighted graph U...")
U = buildGraph(unweightedGraphFile, skipLines=0,
               splitSep=" ", weightedEdges=False)
print(datetime.now(), " --> U: nodes ",
      len(U.nodes()), " edges: ", len(U.edges()))

# Stores the unweighted graph in a pickle file
# nx.write_gpickle(U, unweightedGraphPickle) # UNCOMMENT this line if you want to save a graph

# STEP TWO
# Builds the alignment graph A
print(datetime.now(), " --> build alignment graph A...")
A = pairwiseAlignment(U, W, k=5, simTxt=simFile, skipLines=0, splitSep="-")
print(datetime.now(), " --> alignGraph A: nodes ",
      len(A.nodes()), " edges: ", len(A.edges()))

# Stores the alignment graph in a pickle file
nx.write_gpickle(A, alignmentGraphPickle) # COMMENT this line if you don't want to save a graph

# LAST STEP
# Extracts the DCS from the alignment graph
print(datetime.now(), " --> Search DCS in alignment graph...")
dcsA = extractDCS(A)
# Stores the DCS graph of A in a pickle file
nx.write_gpickle(dcsA, dcsGraphPickle)

t2 = datetime.now()
print(t2, " --> FINISHED")
print("Execution time: ", t2-t1)
