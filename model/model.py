import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.nodi = []
        self.id_map = {}
        self._edges = []
    # carichiamo gli album da insierire nella dd
    def load_album(self,durata):
        album = DAO.get_album_nodes(durata)
        return album
    def build_graph(self,durata):
        self.G.clear()
        self.nodi = DAO.get_album_nodes(durata)
        for n in self.nodi:
            self.G.add_node(n)
            self.id_map[n.id] = n
        self._edges = DAO.get_edges(durata)
        for a1,a2 in self._edges:
            self.G.add_edge(self.id_map[a1], self.id_map[a2])
        print(f'I nodi sono: {self.G.number_of_nodes()}, archi : {self.G.number_of_edges()}')
        return self.G
    def graph_det(self):
        return self.G.number_of_nodes(), self.G.number_of_edges()


    def get_component(self,album):
        r = list(nx.node_connected_component(self.G, album))
        print(r)
        return r












