from models.vehicle import Truck, Car, Helicopter 
import heapq
from itertools import combinations
from itertools import combinations_with_replacement

class UCS:
    def __init__(self, graph):
        """
        Inicializa a classe UCS com o grafo.

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
        """
        Realiza a busca UCS no grafo considerando os veículos disponíveis.

        :param start: Nó inicial.
        :param goal: Nó objetivo.
        :return: Caminho, custo total e lista de veículos usados.
        """
        if start not in self.graph.nodes or goal not in self.graph.nodes:
            raise ValueError(f"O nó {start} ou {goal} não está no grafo.")

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

        visited = set()
        priority_queue = []  # (custo acumulado, nó atual)
        costs = {start: 0}  # Armazena o menor custo para alcançar cada nó
        parent = {start: None}  # Para reconstruir o caminho
        heapq.heappush(priority_queue, (0, start))

        while priority_queue:
            cost, current_node = heapq.heappop(priority_queue)

            if current_node == goal:
                # Reconstruir o caminho a partir dos pais
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = parent[current_node]
                path.reverse()

                # Calcular a combinação ótima de veículos para atender à demanda
                vehicle_combination = self.calculate_vehicle_combination(goal_population, vehicles)
                return path, cost, vehicle_combination

            if current_node not in visited:
                visited.add(current_node)

                for neighbor in self.graph.neighbors(current_node):
                    edge_data = self.graph.get_edge_data(current_node, neighbor)
                    if edge_data.get('closed', False):  # Ignora estradas fechadas
                        continue

                    edge_cost = edge_data.get('weight', 1)  # Distância da estrada
                    new_cost = cost + edge_cost

                    # Atualiza somente se o novo custo for menor ou o nó não tiver sido processado
                    if neighbor not in costs or new_cost < costs[neighbor]:
                        costs[neighbor] = new_cost
                        heapq.heappush(priority_queue, (new_cost, neighbor))
                        parent[neighbor] = current_node

        return None, float('inf'), []  # Nenhum caminho encontrado

