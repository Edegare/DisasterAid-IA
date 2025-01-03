# Arquivo: search/bfs.py

from itertools import combinations_with_replacement
from models.vehicle import Truck, Car, Helicopter

class BFS:
    def __init__(self, graph):
        """
        Inicializa a classe BFS com o grafo.

        :param graph: Grafo representando o mapa.
        """
        self.graph = graph

    def calculate_vehicle_combination(self, population, vehicles):
        """
        Calcula a combinação mais eficiente de veículos para transportar a quantidade necessária de mantimentos.

        :param population: População da zona de ajuda (mantimentos necessários).
        :param vehicles: Lista de veículos disponíveis na zona de suporte.
        :return: Lista de veículos otimizados (tipo e quantidade).
        """
        best_combination = None
        min_excess_capacity = float('inf')
        min_vehicle_count = float('inf')

        # Gerar todas as combinações possíveis de veículos (com repetição)
        for r in range(1, len(vehicles) * 10):  # Multiplicador para permitir mais combinações
            for combo in combinations_with_replacement(vehicles, r):
                total_capacity = sum(vehicle.capacity for vehicle in combo)

                # Verificar se a capacidade atende à necessidade
                if total_capacity >= population:
                    excess_capacity = total_capacity - population
                    vehicle_count = len(combo)

                    # Priorizar combinações com menor excesso e menor número de veículos
                    if excess_capacity < min_excess_capacity or (
                        excess_capacity == min_excess_capacity and vehicle_count < min_vehicle_count
                    ):
                        min_excess_capacity = excess_capacity
                        min_vehicle_count = vehicle_count
                        best_combination = combo

        # Contar os veículos usados na melhor combinação
        vehicle_count = {}
        if best_combination:
            for vehicle in best_combination:
                if vehicle.id in vehicle_count:
                    vehicle_count[vehicle.id]['quantity'] += 1
                else:
                    vehicle_count[vehicle.id] = {'id': vehicle.id, 'quantity': 1}

        return list(vehicle_count.values())

    def search(self, start, goal):
        if start not in self.graph.nodes or goal not in self.graph.nodes:
            raise ValueError(f"O nó {start} ou {goal} não está no grafo.")

        visited = set()
        queue = [[start]]  # Cada entrada é [lista de nós]

        while queue:
            path = queue.pop(0)  # Remove o primeiro caminho da fila
            node = path[-1]  # Último nó no caminho atual

            if node == goal:
                # Calcula o custo total do caminho
                cost = sum(self.graph.get_edge_data(path[i], path[i + 1])['weight']
                           for i in range(len(path) - 1))

                # Obter a população da zona de ajuda
                goal_population = self.graph.nodes[goal].get('population', 0)

                # Obter a lista de veículos disponíveis na zona de suporte
                vehicles = self.graph.nodes[start].get('vehicles', [])
                if isinstance(vehicles, list) and vehicles and isinstance(vehicles[0], dict):
                    vehicles = [
                        Truck(v['id']) if v['type'] == 'truck' else
                        Car(v['id']) if v['type'] == 'car' else
                        Helicopter(v['id']) if v['type'] == 'helicopter' else None
                        for v in vehicles
                    ]
                    vehicles = [v for v in vehicles if v is not None]

                # Calcular a combinação ótima de veículos para atender à demanda
                vehicle_combination = self.calculate_vehicle_combination(goal_population, vehicles)
                return path, cost, vehicle_combination

            if node not in visited:
                visited.add(node)
                for neighbor in self.graph.neighbors(node):
                    edge_data = self.graph.get_edge_data(node, neighbor)
                    edge_cost = edge_data.get('weight', 1)  # Assumir peso 1 se não especificado

                    new_path = list(path)  # Copiar o caminho atual
                    new_path.append(neighbor)
                    queue.append(new_path)

        return None, float('inf'), []  # Nenhum caminho encontrado

