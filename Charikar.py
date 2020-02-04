import networkx as nx
from datetime import datetime


def adjList(G):
    '''Costruisce la lista di adiacenza del grafo G, considerando anche i pesi degli archi.
    G è un grafo pesato e non diretto.
    output: {1:{2:0.5},2:{1:0.5,3:0.6},3:{2:0.2}}'''
    adj = {}
    for e in G.edges:
        if e[0] in adj.keys():
            adj[e[0]][e[1]] = G[e[0]][e[1]]['weight']
        else:
            adj[e[0]] = {e[1]: G[e[0]][e[1]]['weight']}
        if e[1] in adj.keys():
            adj[e[1]][e[0]] = G[e[1]][e[0]]['weight']
        else:
            adj[e[1]] = {e[0]: G[e[1]][e[0]]['weight']}
    return adj


def nodeVol(node):
    '''Calcola il vol di un nodo'''
    vol = 0.0
    for j in node.keys():
        vol = vol+node[j]
    return vol


def density(adj):
    '''Calcola la densità del grafo a partire dalla sua lista di adiacenza.
    La densità in questo caso è calcolata come sommatoria del vol dei nodi, fratto il numero di nodi.'''
    N = len(adj.keys())
    sumVol = 0
    for i in adj.keys():
        for j in adj[i].keys():
            sumVol = sumVol+adj[i][j]
    return sumVol/N


def minVolNode(adj):
    '''Utilizza la lista di adiacenza per trovare il nodo con vol più basso.'''
    minvol = float('inf')
    node = None
    for i in adj.keys():
        vol = nodeVol(adj[i])
        if vol <= minvol:
            minvol = vol
            node = i
    return node

def removeNode(node, adj):
    '''Rimuove un nodo e tutti i suoi archi adiacenti da una lista di adiacenza.'''
    nDict=adj.pop(node)
    for i in nDict.keys():
        adj[i].pop(node)
    return adj

def algorithm_efficient():
    t1=datetime.now()

    G=nx.read_gpickle("../dataset/Gowalla/G_graphA.gz2")

    # algoritmo PRIMO PASSO

    adj = adjList(G)  # costruisce la lista di adiacenza
    current_density = 0  # in questo caso è ladensità iniziale di confronto
    new_density = density(adj)  # calcola la densità di G
    #print("Densità: ",current_density,"-->",new_density)

    # passo RICORSIVO

    # elimino il nodo di grado più basso finchè aumenta la densità del sottografo di G
    while(new_density >= current_density):
        current_density = new_density
        adj_backup=adj.copy()
        # trovo nodo con grado minimo
        n = minVolNode(adj)        
        # rimuovo nodo con grado minimo dalla lista di adiacenza
        adj=removeNode(n,adj)
        new_density = density(adj)
        print("Densità iterazione precedente: ", current_density,
              "--> Densità iterazione corrente", new_density)
        # verifico densità
        if new_density < current_density:
            adj=adj_backup
    nodes=list(adj.keys())
    dcs=G.subgraph(nodes)
    print("Il Sottografo più denso è composta da", len(nodes), "nodi.")
    nx.write_gpickle(dcs,'../dataset/Gowalla/G_dcs.gz2')

    print("Tempo di esecuzione", datetime.now()-t1)




def algorithm():
    t1=datetime.now()
    # # percorso del file txt conntenete gli archi con i relativi pesi
    # path = 'C:/Users/User/Google Drive/densest subgraph algorithm/dataset/RandomGraph/edgesW.txt'
    # # creo grafo networkx a partire da file txt
    # G = nx.Graph()
    # with open(path, 'r') as txt:
    #     for line in txt:
    #         l = line.split()
    #         n1 = int(l[0])
    #         n2 = int(l[1])
    #         w = float(l[2])
    #         G.add_edge(n1, n2, weight=w)
    #         # print([n1,n2,w])

    G=nx.read_gpickle("../dataset/DBLP/DBLP_graphA.gz2")

    # algoritmo PRIMO PASSO

    adj = adjList(G)  # costruisce la lista di adiacenza
    current_density = 0  # in questo caso è ladensità iniziale di confronto
    new_density = density(adj)  # calcola la densità di G
    #print("Densità: ",current_density,"-->",new_density)

    # passo RICORSIVO

    # elimino il nodo di grado più basso finchè aumenta la densità del sottografo di G
    while(new_density > current_density):
        current_density = new_density
        # trovo nodo con grado minimo
        n = minVolNode(adj)
        # rimuovo nodo con grado minimo dal grafo
        G1 = G.copy()  # così ho in G il grafo dell'iterazione precedente ed in G1 il grafo dell'iterazione corrente
        try:
            G1.remove_node(n)
            print("Rimuovo il nodo ", n)
        except:
            print("Nessun nodo rimisso")
            continue
        print("Nodi del nuovo sottografo ", len(G1.nodes))
        # ricalcolo la lista di adiacenza
        adj = adjList(G1)
        # print(adj1)
        # calcolo nuova densità
        new_density = density(adj)
        print("Densità iterazione precedente: ", current_density,
              "--> Densità iterazione corrente", new_density)
        # verifico densità
        if new_density > current_density:
            G = G1.copy()
            # d=new_density
    print("Il Sottografo più denso è composta da", len(G.nodes), "nodi.")
    nx.write_gpickle(G,'../dataset/DBLP/DBLP_dcs.gz2')
    print("Tempo di esecuzione", datetime.now()-t1)

if __name__=='__main__':    
    algorithm_efficient()
