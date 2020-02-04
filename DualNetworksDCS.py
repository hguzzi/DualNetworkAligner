import networkx as nx
from cdlib import algorithms
import matplotlib.pyplot as plt
import sys
import csv
from datetime import datetime


def buildGraph(pathGraph, skipLines=1, splitSep=" ", weightedEdges=False):   
    '''Build a undirected graph from a TXT file.
        Input:
            - pathGraph: TXT file path;
            - skiplines: number of header lines of the TXT file (the function skips these lines) (default: 1);
            - splitSep: separator character to split a line of the TXT file into a list (default: " ");
            - weightedEdges: boolean variable that indicates whether the graph to be constructed is weighed (default: False).
        Output:
            - objGraph: graph of the Graph class of the Networkx library.'''
    #
    # crea il grafo vuoto
    objGraph = nx.Graph(data=True)
    ###
    if(weightedEdges == False):
        # legge il file e crea un grafo non pesato
        # apro il file in sola lettura
        # se il file non può essere aperto lancia un'eccezione
        try:
            f = open(pathGraph, 'r')
        except:
            sys.exit("ERROR! Unable to open file: "+pathGraph)
        # se il file non è vuoto legge riga per riga e costruisce il grafo
        # consideriamo che ogni riga rappresenta una coppia di nodi collegata da un edge
        nLine = 1 # serve per contare le righe del file TXT
        for line in f:
            # ogni riga di un file TXT termina con il carattere di controllo "Line feed" lo elimina
            line = line.replace('\n', '')
            # salta le righe di intestazione del file TXT            
            if(skipLines < nLine):
                lineSplit = line.split(splitSep)
                # if(len(lineSplit) == 2):  # controlla se la lista contiene due stringhe (i due nodi) #posso fare anche con try except per raccogliere tutte le eccezioni
                objGraph.add_edge(lineSplit[0], lineSplit[1])
                # else:
                #sys.exit("ERRORE in una riga del file "+pathGraph)
            else:
                nLine += 1
        f.close()

    else:
        # legge il file e crea un grafo pesato
        try:
            f = open(pathGraph, 'r')
        except:
            sys.exit("ERROR! Unable to open file: "+pathGraph)
        nLine = 1
        for line in f:
            line = line.replace('\n', '')
            if(skipLines < nLine):
                lineSplit = line.split(splitSep)
                # ogni riga deve contenere anche il peso dell'arco
                if(len(lineSplit) == 3):  
                    objGraph.add_edge(
                        lineSplit[0], lineSplit[1], weight=float(lineSplit[2]))
                else:
                    sys.exit("ERROR in a line of the file "+pathGraph)
            else:
                nLine += 1
        f.close()
        # normalizza il peso degli archi del grafo
        objGraph = normWeight(objGraph)    
    return objGraph


def normWeight(objGraph):
    '''Normalize the weight of edges in a graph.
        Input:
            - objGraph: graph of the Graph class of the Networkx library.
        Output:
            - objGraph: normalized graph of the Graph class of the Networkx library.'''
    weight = []
    for i in objGraph.edges():
        weight.append(objGraph.get_edge_data(i[0], i[1])['weight'])
    maxWeight = max(weight)
    for j in objGraph.edges():
        #w = 1.0 - (objGraph.get_edge_data(j[0], j[1])['weight']/maxWeight)
        w = objGraph.get_edge_data(j[0], j[1])['weight']/maxWeight
        objGraph.add_edge(j[0], j[1], weight=w)
    return objGraph


# costruisce file di testo con lista dei nodi corrispondenti tra le due rete n1-n2
def buildSimFile(graph, filePath):
    '''Builds the similarity file of double networks that have nodes with the same label, using the order of the weighted graph nodes as ordering.
        Input:
            - graph: weighted graph;
            - filePath: file name, complete with path, in which to store the similarities.'''
    simList = []
    for i in graph.nodes:
        simList.append([i, i])
    with open(filePath, 'w', encoding='utf-8') as txt:
        for i in simList:
            # nodo rete NON pesata - nodo rete pesata
            txt.write(i[0]+"-"+i[1]+"\n")


# algoritmo di allineamento
def pairwiseAlignment(U, W, k, simTxt, skipLines, splitSep):
    '''Pairwise local aligner for dual networks.
        Input:
            - U: unweighted graph (physical network);
            - W: weighted graph (conceptual network);
            - simTxt: similarity files, example row -> "Unode-Wnode". The TXT file indicates which node of the physical network corresponds in the conceptual network;
            - skipLines: number of header lines of the TXT file simTxt (the function skips these lines);
            - splitSep: separator character to split a line of the TXT file simTxt into a list;
        Output:
            - algnGraph: graph of the Graph class of the Networkx library.'''
    algnGraph = nx.Graph(data=True)
    sim = []
    match = 0
    gap = 0
    with open(simTxt, 'r', encoding='utf-8') as txt:
        nLine = 1
        for row in txt:
            if nLine > skipLines:
                row = row.replace('\n', '')
                # N.B. necessario per la corretta applicazione del metodo Louvain di ricerca delle comunità. 
                # I nodi del grafo di allineamento devono essere inseriti nello stesso ordine di quelli del grafo pesato.        
                algnGraph.add_node(row)  
                n = row.split(splitSep)
                sim.append([n[0], n[1]])
            nLine = nLine+1
    while len(sim) > 1:
        i = sim.pop(0)
        u1 = i[0]
        w1 = i[1]
        a1 = u1+"-"+w1
        for j in sim:
            u2 = j[0]
            w2 = j[1]
            a2 = u2+"-"+w2
            # try:
            if(W.has_edge(w1, w2) == True):
                if(U.has_edge(u1, u2) == True):  # MATCH
                    edgeW = W.get_edge_data(w1, w2)['weight']
                    algnGraph.add_edge(a1, a2, weight=edgeW)
                    match = match+1
                # gap or mismatch
                # se sono adiacenti solo i nodi w1,w2 in graphW
                else:  # GAP o MISMATCH
                    try:
                        path = nx.shortest_path_length(U, u1, u2)  # no pesato
                        # metodo alternativo per il calcolo del peso dell'arco
                        #edgeW = W.get_edge_data(w1, w2)['weight']
                        #d = 1 - (path-1)/k
                        # w = edgeW*d #peso dell'arco del grafo di allineamento
                    except:
                        path = 1000000

                    if(path <= k):  # GAP
                        # solo se la distanza nel grafo non pesato è minore di k aggiunge un arco nel grafo di similarità con peso pari alla distenza (path)
                        edgeW = W.get_edge_data(w1, w2)['weight']
                        algnGraph.add_edge(a1, a2, weight=edgeW)
                        gap = gap+1
                    # else: # MISMATCH
            # else: # MISMATCH
            # except KeyError:
                # continue
    print("Match: ", match, ", Gap: ", gap)
    return algnGraph


# calcola la densità di un grafo
def densityWgraph(W):
    '''Calculate the density of a weighted graph.
        Input:
            - W: weighted graph.
        Output:
            - density: density of the graph.'''
    ww = []
    for i in W.edges():
        ww.append(W.get_edge_data(i[0], i[1])['weight'])
    density = sum(ww)/len(W.nodes())
    return density


# # ritorna dizionario chiave nome comunità, valore [density]
# def comsDict(U, W, NodeClustering):
#     coms = {}
#     for i in range(0, len(NodeClustering.communities)):
#         # Un = []  # node list
#         Wn = []  # node list
#         for j in NodeClustering.communities[i]:
#             n = j.split("-")
#             #u = n[0]
#             # Un.append(u)
#             w = n[1]
#             Wn.append(w)
#         #Un = list(dict.fromkeys(Un))
#         # Us = U.subgraph(Un)  # sottografo di U
#         #c = nx.is_connected(Us)
#         #Wn = list(dict.fromkeys(Wn))
#         Ws = W.subgraph(Wn)  # sottografo di W
#         m = densityWgraph(Ws)
#         coms[i] = {"dWs": m, "Ws": len(Ws.nodes)}
#     return coms


# def extractDCS(U, W, algnGraph, NodeClustering):
#     comDict = comsDict(U, W, NodeClustering)
#     maxCom = 0
#     maxWeight = 0
#     for i in comDict:
#         # if comDict[i]['dWs']> maxWeight and comDict[i]['Uconn']==True:
#         if comDict[i]['dWs'] > maxWeight:
#             maxCom = i
#             maxWeight = comDict[i]['dWs']
#     dcs = algnGraph.subgraph(NodeClustering.communities[maxCom])
#     print(f"DCS --> comunità {maxCom}: {comDict[maxCom]}")
#     return dcs


def extractDCS(U, W, algnGraph):
    '''Extracts the DCS from the alignment graph of the dual networks.
        Input:
            - U: unweighted graph (physical network);
            - W: weighted graph (conceptual network);
            - algnGraph: alignment graph.
        Output:
            - subDCS: DCS of the alignment graph. Subgraph induced on the nodes of the densest community of the alignment graph;
            - subU: subgraph of the physical network induced on DCS nodes.
            - subW: subgraph of the conceptual network induced on DCS nodes.
    '''
    # algoritmo di Louvain per estrarre le comunità dal grafo di allineamento
    NodeClustering = algorithms.louvain(
        algnGraph, weight='weight', resolution=1., randomize=False)
    maxWeight = 0
    dcs = []
    Un = []  # inizzializzo lista nodi del sottografo di U del DCS
    Wn = []  # inizzializzo lista nodi del sottografo di W del DCS
    for i in NodeClustering.communities:  # itero le comunità
        Unt = []  # lista temporanea  # inizzializzo lista nodi del sottografo di U contenuti nella comunità i
        Wnt = []  # lista temporanea # inizzializzo lista nodi del sottografo di W contenuti nella comunità i
        for j in i:  # itero i nodi della comunità i
            # divido il nome del nodo per estrarre il relativo nodo di U e W
            a = j.split("-")
            u = a[0]  # nodo rete non pesata
            Unt.append(u)
            w = a[1]  # nodo rete pesata
            Wnt.append(w)
        # calcolo densità del sottografo di W
        if len(Wnt) > 0:
            subWt = W.subgraph(Wnt)  # crea sottografo
            if len(subWt.nodes) > 0:
                dWs = densityWgraph(subWt)
            else:
                dWs = 0
        else:
            dWs = 0
        if dWs > maxWeight:
            maxWeight = dWs
            dcs = i.copy()
            Un = Unt.copy()
            Wn = Wnt.copy()
    subDCS = algnGraph.subgraph(dcs)
    subU = U.subgraph(Un)
    subW = W.subgraph(Wn)
    print("DCS --> nodes: ", len(subDCS.nodes), ", edges: ",
          len(subDCS.edges), ", density: ", maxWeight)
    return subDCS, subU, subW


# estrae la comunità più densa di un grafo
def densestCommunity(graph):
    '''Extracts the densest community of a graph.
        Input:
            - graph: weighted graph.
        Output:
            - graphDC: subgraph induced on the nodes of the densest community of the graph.'''
    # algoritmo di Louvain per estrarre le comunità dal grafo
    NodeClustering = algorithms.louvain(
        graph, weight='weight', resolution=1., randomize=False)
    maxWeight = 0
    dcs = []
    for i in NodeClustering.communities:
        Sg = graph.subgraph(i)
        dWs = densityWgraph(Sg)
        if dWs > maxWeight:
            maxWeight = dWs
            dcs = i.copy()
    graphDC = graph.subgraph(dcs)
    print("Densest Community of weighted graph --> nodes: ", len(graphDC.nodes), ", edges: ",
          len(graphDC.edges), "; density: ", maxWeight)
    return graphDC


def main():
    inputFile = "9606.protein.links.v11.0.txt"
    simFile = "HS_simFile.txt"
    print(datetime.now(), " --> build weighted graph W...")
    W = buildGraph(inputFile, weightedEdges=True)
    nx.write_gpickle(W, "HS_graphW.gz2")
    print(datetime.now(), " --> W: nodes ",
          len(W.nodes()), " edges: ", len(W.edges()))
    print(datetime.now(), " --> build unweighted graph U...")
    U = buildGraph(inputFile, weightedEdges=False)
    nx.write_gpickle(U, "HS_graphU.gz2")
    print(datetime.now(), " --> U: nodes ",
          len(U.nodes()), " edges: ", len(U.edges()))
    print(datetime.now(), " --> build alignment graph A...")
    A = pairwiseAlignment(U, W, k=5, simTxt=simFile, skipLines=0, splitSep="-")
    nx.write_gpickle(A, "HS_graphA.gz2")
    print(datetime.now(), " --> alignGraph A: nodes ",
          len(A.nodes()), " edges: ", len(A.edges()))
    print(datetime.now(), " --> Search DCS in alignment graph...")
    dcsA, subU, subW = extractDCS(U, W, A)
    nx.write_gpickle(dcsA, "HS_dcsA.gz2")
    nx.write_gpickle(subU, "HS_subU.gz2")
    nx.write_gpickle(subW, "HS_subW.gz2")
    print(datetime.now(), "Search DCS of weighted graph W...")
    dcsW = densestCommunity(W)
    nx.write_gpickle(dcsW, "HS_dcsW.gz2")


if __name__ == "__main__":
    main()
