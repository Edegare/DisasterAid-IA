import networkx as nx
from geopy.distance import geodesic
import json
import matplotlib.pyplot as plt
import sys
import os

# Adicionar a raiz do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MapGenerator:
    def __init__(self, json_path):
        """
        Inicializa o gerador de mapas com o caminho para o ficheiro JSON das zonas.

        :param json_path: Caminho para o ficheiro JSON com os dados das zonas.
        """
        self.json_path = json_path
        self.graph = nx.Graph()

    @staticmethod
    def calculate_distance(coord1, coord2):
        """
        Calcula a distância entre duas coordenadas geográficas (linha reta).

        :param coord1: Tuplo com (latitude, longitude) do ponto 1.
        :param coord2: Tuplo com (latitude, longitude) do ponto 2.
        :return: Distância em quilómetros.
        """
        return geodesic(coord1, coord2).kilometers

    def load_zones(self):
        """
        Carrega os dados das zonas a partir do ficheiro JSON, cria o grafo
        e devolve as zonas de suporte.

        :return: Lista de zonas de suporte (IDs).
        """
        with open(self.json_path, "r") as file:
            zones_data = json.load(file)

        # Adicionar nós e coordenadas ao grafo
        for zone in zones_data:
            self.graph.add_node(zone["id"], 
                                latitude=zone["latitude"], 
                                longitude=zone["longitude"], 
                                zone_type=zone["zone_type"], 
                                accessibility=zone["accessibility"], 
                                vehicles=zone["vehicles"],
                                critical_time=zone.get("critical_time"),
                                population=zone.get("population", 0),
                                priority=zone.get("priority", 0))

        # Adicionar arestas com as distâncias
        for zone in zones_data:
            current_zone_id = zone["id"]
            current_coords = (zone["latitude"], zone["longitude"])
            for accessible_zone_id in zone["accessible_zones"]:
                # Encontrar a zona de destino
                destination_zone = next(z for z in zones_data if z["id"] == accessible_zone_id)
                destination_coords = (destination_zone["latitude"], destination_zone["longitude"])
                # Calcular a distância
                distance = self.calculate_distance(current_coords, destination_coords)
                # Adicionar aresta ao grafo
                self.graph.add_edge(current_zone_id, accessible_zone_id, weight=distance)


    def display_graph(self):
        """
        Mostra o grafo criado em formato gráfico.
        """
        pos = {node: (self.graph.nodes[node]['longitude'], self.graph.nodes[node]['latitude']) for node in self.graph.nodes}
        plt.figure(figsize=(10, 8))
        nx.draw(self.graph, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold")
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels={k: f"{v:.2f} km" for k, v in labels.items()})
        plt.title("Mapa de Zonas e Distâncias")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.show()

    # Supondo que o grafo já foi gerado e contém o atributo 'zone_type'
    def get_zones_by_type(self, zone_type):
        """
        Retorna uma lista de zonas de um determinado tipo.

        :param graph: Grafo com os dados das zonas.
        :param zone_type: Tipo de zona (e.g., "supply", "support", "normal").
        :return: Lista de IDs das zonas que correspondem ao tipo especificado.
        """
        return [node for node, attrs in self.graph.nodes(data=True) if attrs.get('zone_type') == zone_type]

# Exemplo de utilização
if __name__ == "__main__":
    from search.bfs import BFS
    from search.dfs import DFS
    from search.greedy import GreedyBestFirstSearch
    from search.astar import AStar

    map_generator = MapGenerator(json_path="../input/braga_zones.json")
    map_generator.load_zones()
    map_generator.display_graph()
    graph = map_generator.graph

    bfs = BFS(graph)
    dfs = DFS(graph)
    greedy = GreedyBestFirstSearch(graph)
    astar = AStar(graph)

    start_node = "Esposende"
    goal_node = "Celorico de Basto"

    print("BFS Path:", bfs.search(start_node, goal_node))
    print("DFS Path:", dfs.search(start_node, goal_node))
    print("Greedy Path:", greedy.search(start_node, goal_node))
    print("A* Path:", astar.search(start_node, goal_node))
