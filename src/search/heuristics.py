from geopy.distance import geodesic

class Heuristics:
    @staticmethod
    def straight_line_distance(graph, node, goal):
        """
        Calcula a distância em linha reta (heurística) entre dois nós.

        :param graph: Grafo contendo os nós.
        :param node: Nó atual.
        :param goal: Nó objetivo.
        :return: Distância em linha reta entre o nó atual e o objetivo.
        """
        node_coords = (graph.nodes[node]['latitude'], graph.nodes[node]['longitude'])
        goal_coords = (graph.nodes[goal]['latitude'], graph.nodes[goal]['longitude'])
        return geodesic(node_coords, goal_coords).kilometers
