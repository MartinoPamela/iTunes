import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestSet = None
        self._bestScore = 0

    def getSetAlbum(self, a1, dTOT):

        self._bestSet = None
        self._bestScore = 0

        connessa = nx.node_connected_component(self._graph, a1)
        # pool di nodi da cui posso attingere per costruire il set
        parziale = set([a1])
        connessa.remove(a1)  # a1 sarà incluso in connessa e dato che non voglio ripetizioni perché è un set lo rimuovo

        self._ricorsione(parziale, connessa, dTOT)

        return self._bestSet, self.durataTot(self._bestSet)

    def _ricorsione(self, parziale, connessa, dTOT):

        # verificare se parziale è una soluzione ammissibile
        if self.durataTot(parziale) > dTOT:
            return  # unica condizione in cui posso uscire, ovvero la scarto se è >

        # se ho superato questo if vuol dire che parziale ancora può ammettere nuovi nodi, ma prima di fare la
        # ricorsione vado a vedere se parziale è effettivamente l'ottimo rispetto a quello che ho trovato finora

        # verificare se parziale è migliore del best

        if len(parziale) > self._bestScore:  # vuol dire che ho trovato una soluzione migliore
            self._bestSet = copy.deepcopy(parziale)
            self._bestScore = len(parziale)
            # non devo fare una return perché non ha senso uscire, ho solo detto che la soluzione
            # è migliore di quella precedente, ma posso ancora aggiungere nodi idealmente

        # ciclo su nodi aggiungibili -- ricorsione
        for c in connessa:
            if c not in parziale:  # mi conviene fare questo controllo per evitare un'iterazione in più
                parziale.add(c)
                # rimanenti = copy.deepcopy(connessa)
                # rimanenti.remove(c)
                self._ricorsione(parziale, connessa, dTOT)  # così accorcio i cicli che faccio dentro la ricorsione
                parziale.remove(c)

        """
        faccio prima il primo if perché prima verifico che parziale sia effettivamente una soluzione valida, e poi
        provo a salvarla con il best, facessi il contrario rishcierei di salvare una soluzione ottima che però 
        non rispetta i requisiti (in questo caso andrei a salvare nella best una parziale che ha una durata più 
        lunga potenzialmente di dTOT)
        """

    def durataTot(self, listOfNodes):  # listOfNodes è una lista di album
        dtot = 0
        for n in listOfNodes:
            dtot += n.totD
        return toMinutes(dtot)

    def buildGraph(self, d):  # quando ho nodi che dipendono dall'utente non posso farlo nell'init
        self._graph.clear()
        self._graph.add_nodes_from(DAO.getAlbums(toMillisec(d)))
        self._idMap = {a.AlbumId: a for a in self._graph.nodes}

        # for a in list(self._grafo.nodes):
        #    self._idMap[a.AlbumId] = a

        edges = DAO.getEdges(self._idMap)

        self._graph.add_edges_from(edges)  # questo metodo vuole una lista di tuple

    def getConnessaDetails(self, v0):
        conn = nx.node_connected_component(self._graph, v0)
        durataTot = 0
        for album in conn:
            durataTot += toMinutes(album.totD)  # totD è in millisecondi quindi ho bisogno di convertirli in minuti
            # sommo le durate dei singoli album che fanno parte della componente connessa

        return len(conn), durataTot

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getNodes(self):
        return list(self._graph.nodes)

    def getGraphSize(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getNodeI(self, i):  # metodo che mi dà un nodo per non accedere al grafo direttamente
        print(self._idMap[i])
        return self._idMap[i]


def toMillisec(d):
    return d*60*1000


def toMinutes(d):
    return d/1000/60
