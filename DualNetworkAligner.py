# gestione dei grafi
import networkx as nx

# calcolo del tempo di esecuzione
from datetime import datetime

# vari
import sys


def main():

    # path
    graphFile1, graphFile2 = "graph1.txt", "graph2.txt"
    # nodesFile1, nodesFile2 = "nodes1.txt", "nodes2.txt"
    similarityFile = "similarityFile.txt"
    outFile = "outFile.txt"
    logFile = "log.txt"

    # coefficiente per il calcolo dello shotest path di archi pesati
    k = 10

    # crea due oggetti di tipo Graph vuoti
    # g1 = nx.Graph(data=True)
    # g2 = nx.Graph(data=True)

    # costruisce g1 e g2, leggendo il file txt corrispondente
    g1 = buildGraph(graphFile1, 0)
    g2 = buildGraph(graphFile2, 0)

    # costruisce il grafo di allineamento
    al2 = buildAlignmentGraphFormSimilarityFile(similarityFile, g1, g2, k)


def buildGraph(pathGraph, skipLines, splitSep=" ", weightedEdges=False):
    # se ritorno direttamente il grafo posso evitare di creare il grafo vuoto precedentemente #return objGraph
    '''Funzione che ritorna un oggetto di tipo networkx.Graph.
        Input:
            - pathGraph: path del file txt contenente le info di costruzione del grafo;
            - skiplines: righe da saltare all'interno del file ;
            - splitSep: carattere di separazione per lo split della riga (default: " ");
            - weightedEdges: booleano  che indica se gli archi del grafo sono pesati (default: False).
        Output:
            - objGraph: oggetto networkx Graph.'''
    #
    # crea il grafo vuoto
    objGraph = nx.Graph(data=True)
    ###
    if(weightedEdges == False):
        # legge il file e crea l'oggetto Graph non pesato
        # apro il file in sola lettura
        # gestire eccezione se il path è bagliato try except
        try:
            f = open(pathGraph, 'r')
        except:
            sys.exit("ERRORE! impossibile aprire il file: "+pathGraph)
        # se il file non è vuoto legge riga per riga e costruisce il grafo
        # split() senza argomento fa lo split della stringa usando lo spazio come separatore
        # consideriamo che ogni riga rappresenta una coppia di nodi collegata da un edge
        nLine = 1
        for line in f:
            if(skipLines > nLine):
                lineSplit = line.split()  # lista #se cambio separtore ho una sola riga da modificare
                lineSplit = line.split(splitSep)
                if(len(lineSplit) == 2):  # controlla se la lista contiene due stringhe (i due nodi) #posso fare anche con try except per raccogliere tutte le eccezioni
                    objGraph.add_edge(lineSplit[0], lineSplit[1])
                else:
                    sys.exit("ERRORE in una riga del flie "+pathGraph)
            else:
                nLine += 1

            #f = open(pathGraph, 'r')
            # lineSplit = line.split()  # lista #se cambio separtore ho una sola riga da modificare
            #objGraph.add_edge(lineSplit[0], lineSplit[1])

        f.close()

    else:
        # legge il file e crea l'oggetto Graph pesato
        try:
            f = open(pathGraph, 'r')
        except:
            sys.exit("ERRORE! impossibile aprire il file: "+pathGraph)
        for line in f:
            if(skipLines > nLine):
                lineSplit = line.split()  # lista #se cambio separtore ho una sola riga da modificare
                lineSplit = line.split(splitSep)
                if(len(lineSplit) == 3):  # controlla se la lista contiene due stringhe (i due nodi) #posso fare anche con try except per raccogliere tutte le eccezioni
                    objGraph.add_edge(lineSplit[0], lineSplit[1], lineSplit[2])
                else:
                    sys.exit("ERRORE in una riga del flie "+pathGraph)
            else:
                nLine += 1

            #f = open(pathGraph, 'r')
            # lineSplit = line.split()  # lista #se cambio separtore ho una sola riga da modificare
            # objGraph.add_edge(lineSplit[0], lineSplit[1], weight=lineSplit[2])

        f.close()

    #
    return objGraph

# funzione che crea il grafo di similarità


def buildAlignmentGraphFormSimilarityFile(pathSimFile, graphU, graphW, k, skiplines=0, splitSep=" "):
    '''Ritorna il grafo di similarità'''

    # Graph.has_edge(u, v)	Returns True if the edge (u, v) is in the graph.
    objSimGraph = nx.Graph(data=True)

    f = open(pathSimFile, 'r')

    for line in f:
            # il file contiene le coppie di nodi dei due grafi che costituiscono il nodo del grafo di allineamento
        lineSplit = line.split()
        newNode = lineSplit[0]+"-"+lineSplit[1]
        objSimGraph.add_node(newNode)

    # aggiunge edge alle coppie di nodi
    for i in objSimGraph.nodes():
        for j in objSimGraph.nodes():

            # coppia di nodi del grafo non pesato
            u1 = i.split('-')[0]
            u2 = j.split('-')[0]

            # coppia di nodi del grafo pesato
            w1 = i.split('-')[1]
            w2 = j.split('-')[1]

            # match
            if(graphU.has_edge(u1, u2) == True and graphW.has_edge(w1, w2) == True):
                edgeW = graphW.get_edge_data(w1, w2)['weight']
                objSimGraph.add_edge(i, j, weight=edgeW)
            else:  # gap #mismatch

                try:
                    path = nx.shortest_path_length(graphU, u1, u2)  # no pesato
                except:
                    path = 1000000

                if(path <= k):
				#solo se la distanza nel grafo non pesato è minore di k aggiunge un arco nel grafo di similarità con peso pari alla distenza (path)
                    objSimGraph.add_edge(i, j, weight=path)
                #else:
                    #objSimGraph.add_edge(i, j, weight=1000000)

                # fare funzione che calcola distanza del non pesato e confrontarlo con k per il momento arbitrario
                # https://networkx.github.io/documentation/networkx-2.3/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.shortest_path_length.html#networkx.algorithms.shortest_paths.generic.shortest_path_length
                # nx.shortest_path_length(graphW, w1, w2, weight='weight')  # pesato

    return objSimGraph
