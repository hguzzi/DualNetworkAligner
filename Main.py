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
t1 = datetime.now()
# Folder with the name of dataset to analize
datasetNameFolder = "STRING/"  # <-- MODIFY to select dataset
# Directory path of dataset to analize
inputDirectotyPath = "Dataset/"+datasetNameFolder + "Input/"  
# Directory path to store results
outputDirectoryPath = "Dataset/"+datasetNameFolder + "Output/"  

# INPUT file
# Text file of weighted graph
weightedGraphFile = inputDirectotyPath+"weightedGraph.txt" 
print(weightedGraphFile)
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

print(datetime.now(), " --> build weighted graph W...")
# Builds the weighted graph W
W = buildGraph(weightedGraphFile, skipLines=0,
               splitSep=" ", weightedEdges=True)
# Stores the weighted graph in a pickle file
nx.write_gpickle(W, weightedGraphPickle)
print(datetime.now(), " --> W: nodes ",
      len(W.nodes()), " edges: ", len(W.edges()))

print(datetime.now(), " --> build unweighted graph U...")
# Builds the unweighted graph U
U = buildGraph(unweightedGraphFile, skipLines=0,
               splitSep=" ", weightedEdges=False)
# Stores the unweighted graph in a pickle file
nx.write_gpickle(U, unweightedGraphPickle)
print(datetime.now(), " --> U: nodes ",
      len(U.nodes()), " edges: ", len(U.edges()))

print(datetime.now(), " --> build alignment graph A...")
# Builds the alignment graph A
A = pairwiseAlignment(U, W, k=5, simTxt=simFile, skipLines=0, splitSep="-")
# Stores the alignment graph in a pickle file
nx.write_gpickle(A, alignmentGraphPickle)
print(datetime.now(), " --> alignGraph A: nodes ",
      len(A.nodes()), " edges: ", len(A.edges()))

print(datetime.now(), " --> Search DCS in alignment graph...")
# Extracts the DCS from the alignment graph
dcsA = extractDCS(A)
# Stores the DCS graph of A in a pickle file
nx.write_gpickle(dcsA, dcsGraphPickle)

print("Execution time: ", datetime.now()-t1)
