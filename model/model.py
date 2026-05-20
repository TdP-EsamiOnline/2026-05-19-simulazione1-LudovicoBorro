import networkx as nx
from database.DAO import DAO

class Model:

    def __init__(self):
        self._graph = nx.DiGraph()
        artistiWPop = DAO.getArtistiWPopularity()
        self._idMapArtistiWPop = {}
        for tupla in artistiWPop:
            self._idMapArtistiWPop[tupla[0]] = tupla[1]

    def build_graph(self, genre_id: int):
        nodes = DAO.getAllArtistsByGenre(genre_id)
        self._graph.add_nodes_from(nodes)
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

    @staticmethod
    def getAllGenres():
        return DAO.getAllGenres()

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    @staticmethod
    def _hasEdge(genre_id, artist1_id, artist2_id):
        print(f"Passando al DAO artist1: {artist1_id}, artist2: {artist2_id} e genre: {genre_id}")
        if artist1_id == artist2_id:
            return False

        customers1 = DAO.getCustomerByArtistAndGenre(artist1_id, genre_id)
        customers2 = DAO.getCustomerByArtistAndGenre(artist2_id, genre_id)

        if customers1:
            print("Customers1: "+ str(customers1))
        if customers2:
            print("Customers2: "+ str(customers2))

        for c in customers1:
            if c in customers2:
                print("Esiste un acquirente che ha acquistato da entrambi gli artisti!")
                return True
        return False

    def _getPopolarita(self, artist):
        return self._idMapArtistiWPop.get(artist.ArtistId)

    def getArtistInfluente(self):
        best_artist = None
        best_influence = 0
        for node in self._graph.nodes:
            pass