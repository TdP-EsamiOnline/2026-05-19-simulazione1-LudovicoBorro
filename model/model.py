import networkx as nx
from database.DAO import DAO
import copy
import random

class Model:

    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapArtistiWPop = {}
        self._bestPath = []
        self._bestObjVal = 0
        # self._idMapArtist = {}
        # artists = DAO.getAllArtists()
        # for a in artists:
        #     self._idMapArtist[a.ArtistId] = a

    def getPath(self, v0):
        self._bestPath = []
        self._bestObjVal = 0
        parziale = [v0]

        for v in self._graph.neighbors(v0):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

        return self._bestPath, self._bestObjVal

    def _ricorsione(self, parziale):
        # Condizione di ottimalita
        if len(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = len(parziale)

        # Condizione di terminazione

        # Ricorsione con backtracking
        for v in self._graph.neighbors(parziale[-1]):
            # In realtà questa condizione è sempre falsa, perchè i vicini dell'ultimo nodo aggiunto (cioè i successori) hanno necessariamente
            # peso minore o uguale per costruzione. Infatti gli archi vanno dall'artista che ha popolarità maggiore a quello che ha popolarità
            # minore e se il peso è ottenuto dalla somma delle due popolarità. Di conseguenza la soluzione sarà al massimo di due nodi, v0
            # e un suo vicino, preso grazie la primo ciclo.
            if self._graph[parziale[-2]][parziale[-1]]["weight"] < self._graph[parziale[-1]][v]["weight"] and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def build_graph(self, genre_id: int):
        self._graph.clear()
        nodes = DAO.getAllArtistsByGenre(genre_id)
        self._graph.add_nodes_from(nodes)
        artistiWPop = DAO.getArtistiWPopularityByGenre(genre_id)
        for tupla in artistiWPop:
            self._idMapArtistiWPop[tupla[0]] = tupla[1]
        self._addEdges(genre_id)

    def _addEdges(self, genre_id):
        for u in self._graph.nodes:
            for v in self._graph.nodes:
                if self._hasEdge(genre_id, u.ArtistId, v.ArtistId):
                    popolarita_u = self._getPopolarita(u)
                    popolarita_v = self._getPopolarita(v)
                    if popolarita_u > popolarita_v:
                        self._graph.add_edge(u, v, weight=popolarita_u+popolarita_v)
                    elif popolarita_u < popolarita_v:
                        self._graph.add_edge(v, u, weight=popolarita_v+popolarita_u)
                    else:
                        self._graph.add_edge(u, v, weight=popolarita_u+popolarita_v)
                        self._graph.add_edge(v, u, weight=popolarita_v+popolarita_u)

    # def _addEdgesV2(self, genre_id):
    #     edges = DAO.getAllEdges(genre_id, self._idMapArtist)
    #     for e in edges:
    #         u = e[0]
    #         v = e[1]
    #         pop_u = self._getPopolarita(u)
    #         pop_v = self._getPopolarita(v)
    #         peso = pop_u + pop_v
    #         if pop_u > pop_v:
    #             self._graph.add_edge(u, v, weight=peso)
    #         elif pop_u < pop_v:
    #             self._graph.add_edge(v, u, weight=peso)
    #         else:
    #             self._graph.add_edge(u, v, weight=peso)
    #             self._graph.add_edge(v, u, weight=peso)

    @staticmethod
    def getAllGenres():
        return DAO.getAllGenres()

    @staticmethod
    def getAllArtistByGenre(genre_id):
        return DAO.getAllArtistsByGenre(genre_id)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    @staticmethod
    def _hasEdge(genre_id, artist1_id, artist2_id):
        if artist1_id == artist2_id:
            return False

        customers1 = DAO.getCustomerByArtistAndGenre(artist1_id, genre_id)
        customers2 = set(DAO.getCustomerByArtistAndGenre(artist2_id, genre_id))

        for c in customers1:
            if c in customers2:
                return True
        return False

    def _getPopolarita(self, artist):
        return self._idMapArtistiWPop.get(artist.ArtistId)

    def getArtistInfluente(self):
        best_artist = None
        best_influence = 0
        for node in self._graph.nodes:
            somma_entranti = 0
            somma_uscenti = 0
            for succ in self._graph.successors(node):
                somma_uscenti += self._graph[node][succ]["weight"]
            for prec in self._graph.predecessors(node):
                somma_entranti += self._graph[prec][node]["weight"]
            if somma_uscenti - somma_entranti > best_influence:
                best_artist = node
                best_influence = somma_uscenti - somma_entranti
        return best_artist, best_influence

    def getArchi(self):
        archi = []
        for edge in self._graph.edges:
            u = edge[0]
            v = edge[1]
            peso = self._graph[u][v]["weight"]
            archi.append((u, v, peso))
        archi.sort(key=lambda x: x[2], reverse=True)
        return archi

    def getRandomNode(self):
        index = random.randint(0, len(self._graph.nodes))
        nodi = list(self._graph.nodes)
        return nodi[index]