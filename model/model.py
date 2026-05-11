import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodes = DAO.getAllNodes()  # recupero tutti i nodi dalla query
        self.idMap_ArtObjects = { }
        for n in self._nodes:
            self.idMap_ArtObjects[n.object_id] = n
        self._optPath = []
        self._optCost = 0

    def getOptPath(self, source, lun):
        parziale = [source]
        for n in self._grafo.neighbors(source):
            if n.classification== parziale[-1].classification:
                parziale.append(n)
                self.ricorsione(parziale, lun)
                parziale.pop() # backtracking
        return self._optPath, self._optCost

    def ricorsione(self, parziale, lun):
        if len(parziale) == lun:
            # verifico che la parziale si meglio del mio best (ottimalità)
            if self.costoPath(parziale) > self._optCost:
                self._optCost = self.costoPath(parziale)
                self._optPath = copy.deepcopy(parziale) # fai sempre la copia profonda della soluzione
            return # in ogni caso devo uscire

        # len(parziale) non è ancora uguale a LUN , posso ancora aggiungere nodi
        for n in self._grafo.neighbors(parziale[-1]):
            # ciclo sui vicini dell'ultimo nodo aggiunto
            if parziale[-1].classification == n.classification:
                parziale.append(n)
                self.ricorsione(parziale, lun)
                parziale.pop()  # backtracking


    def costoPath(self, path):
        # calcola la somma dei pesi
        tot=0
        for i in range(0, len(path)-1):
            tot+= self._grafo[path[i]][path[i+1]]["weight"]
            # [nodoPartenza][nodoArrivo][peso]
        return tot


    def getInfoConnessa(self, id_oggetto):        # gli devo passare un id dell'oggetto
        # cerca la componente connessa che contiene id_oggetto
        # guardo nella documentazione di depth-first-search
        if  not self.hasNode(id_oggetto): # id_oggetto potrebbe non essere contenuto nel grafo....
            return None
        source = self.idMap_ArtObjects[id_oggetto]

        # STRATEGIA 1
        dfsTree = nx.dfs_tree(self._grafo, source)
        print("size connessa con dfs_Tree ", len(dfsTree.nodes()))

        # STRATEGIA 2
        dfs_Predecessori  = nx.dfs_predecessors(self._grafo, source)
        print("size connessa con dfs_predecessors ", len(dfs_Predecessori.values()))
        # essendo i predecessori, scarto l'ultimo nodo (dovrei aggiungerne 1)

        # STRATEGIA 3 (quella da usare!)
        conn = nx.node_connected_component(self._grafo, source)
        print("size connessa con node_connected_component ", len(conn))
        return len(conn)



    def hasNode(self, id_oggetto):
        return id_oggetto in self.idMap_ArtObjects



    # =====================COSTRUZIONE DEL GRAFO ==============================================
    def buildGraph(self):
        self._grafo.clear()
        # 1) aggiunge i nodi
        self._grafo.add_nodes_from(self._nodes) # li aggiungo
        # 2) aggiunge gli archi (collegano due oggetti espesti contemporaneamente in una exibition)
        self.addEdges2()  # uso il metodo più efficiente


    # ======================= METODO CHE AGGIUNGONO GLI ARCHI =================================
    def addEdges(self):  # --> METODO INEFFICIENTE (con doppio ciclo)
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getEdgesPeso(u,v)
                if peso is not None:
                    self._grafo.add_edge(u, v, weight=peso)
                    #print(f"aggiunto arco fra {u} e {v} con peso {peso}")

    # METODO PIU' EFFICIENTE !!!
    def addEdges2(self):   # è cambiata la query
        allEdges = DAO.getAllEdges(self.idMap_ArtObjects)
        for e in allEdges:
            self._grafo.add_edge(e.o1, e.o2, weight=e.peso)
            # creo un arco che parte da o1 e finisce in o2

    def getNodeFromId(self, id_oggetto):
        return self.idMap_ArtObjects[id_oggetto]

    # ======================NUMERO DI ARCHI E NODI ==============================
    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)
