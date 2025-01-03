# map/mapGenerator.py

from geopy.distance import geodesic

import random
import networkx as nx
import json
import matplotlib.pyplot as plt
import sys
import os

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
                self.graph.add_edge(
                    current_zone_id, 
                    accessible_zone_id, 
                    weight=distance, 
                    closed= (random.random() < 0.1)  # chance da estrada estar fechada (Se o valor no intervalo [0, 1] for menor do que 0.1 então a estrada fica fechada; se for está aberta)
                )

    def display_graph(self, path=None):
        """
        Mostra o grafo criado em formato gráfico com as coordenadas reais e,
        opcionalmente, destaca um caminho específico.

        :param path: Lista de nós representando o caminho a destacar.
        """
        # Usar as coordenadas reais para posicionar os nós
        pos = {
            node: (self.graph.nodes[node]['longitude'], self.graph.nodes[node]['latitude'])
            for node in self.graph.nodes
        }

        plt.figure(figsize=(12, 10))

        # Separar os nós por tipo
        normal_nodes = [node for node, data in self.graph.nodes(data=True) if data['zone_type'] == 'normal']
        supply_nodes = [node for node, data in self.graph.nodes(data=True) if data['zone_type'] == 'supply']
        support_nodes = [node for node, data in self.graph.nodes(data=True) if data['zone_type'] == 'support']

        # distinguir estradas fechadas das abertas
        closed_edges = [(u, v) for u, v, d in self.graph.edges(data=True) if d.get('closed', False)]
        open_edges = [(u, v) for u, v, d in self.graph.edges(data=True) if not d.get('closed', False)]

        # Desenho dos nós
        nx.draw_networkx_nodes(self.graph, pos, nodelist=normal_nodes, node_color="skyblue", label="Normal", node_size=500)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=supply_nodes, node_color="green", label="Supply", node_size=500)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=support_nodes, node_color="orange", label="Support", node_size=500)

        # Desenho de arestas (estradas abertas e fechadas)
        nx.draw_networkx_edges(self.graph, pos, edgelist=open_edges, edge_color="black", width=1.5)
        nx.draw_networkx_edges(self.graph, pos, edgelist=closed_edges, edge_color="red", width=2.5, style="dashed")

        # Destacar o caminho, se fornecido
        if path:
            path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, edge_color="blue", width=3.5)
            nx.draw_networkx_nodes(self.graph, pos, nodelist=path, node_color="yellow", label="Path Nodes", node_size=700)

        # Desenho de etiquetas dos nós
        nx.draw_networkx_labels(self.graph, pos, font_size=10, font_weight="bold")

        # Etiquetas das distâncias nas arestas
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels={k: f"{v:.2f} km" for k, v in labels.items()}, font_size=8)

        # Adicionar legenda
        plt.legend(scatterpoints=1)
        plt.title("Mapa de Zonas e Distâncias")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.show()

    def get_zones_by_type(self, zone_type):
        """
        Retorna uma lista de zonas de um determinado tipo.

        :param graph: Grafo com os dados das zonas.
        :param zone_type: Tipo de zona (e.g., "supply", "support", "normal").
        :return: Lista de IDs das zonas que correspondem ao tipo especificado.
        """
        return [node for node, attrs in self.graph.nodes(data=True) if attrs.get('zone_type') == zone_type]

