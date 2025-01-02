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
        from itertools import combinations_with_replacement

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
            # Converter os dicionários em objetos Vehicle
            vehicles = [
                Truck(v['id']) if v['type'] == 'truck' else
                Car(v['id']) if v['type'] == 'car' else
                Helicopter(v['id']) if v['type'] == 'helicopter' else None
                for v in vehicles
            ]
            vehicles = [v for v in vehicles if v is not None]

        visited = set()
        priority_queue = []  # (custo acumulado, nó atual)
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
                    if edge_data.get('closed', False):  # Se a estrada estiver fechada
                        continue  # Pular este vizinho
                    
                    edge_cost = edge_data.get('weight', 1)

                    # Calcular o custo acumulado para o vizinho
                    new_cost = cost + edge_cost

                    # Adicionar o vizinho à fila de prioridade com o novo custo
                    if neighbor not in visited:
                        heapq.heappush(priority_queue, (new_cost, neighbor))
                        # Guardar o pai do nó para reconstrução do caminho
                        if neighbor not in parent:
                            parent[neighbor] = current_node

        return None, float('inf'), []  # Nenhum caminho encontrado
# CÓDIGO SÓ PARA AJUDAR ------------------------------------------------------
    def search_vehicle(self, start, goal, vehicle):
        """
        Realiza a busca UCS no grafo considerando o consumo de combustível e reabastecimento.

        :param start: Nó inicial.
        :param goal: Nó objetivo.
        :param vehicle: Veículo utilizado na busca.
        :return: Caminho, custo total, e consumo de combustível.
        """
        if start not in self.graph.nodes or goal not in self.graph.nodes:
            raise ValueError(f"O nó {start} ou {goal} não está no grafo.")

        visited = set()
        priority_queue = []  # (custo acumulado, nó atual, combustível restante, combustível gasto)
        parent = {start: None}  # Para reconstruir o caminho
        heapq.heappush(priority_queue, (0, start, vehicle.fuel_capacity, 0))  # Inicia com tanque cheio


        need_to_fuel = False

        while priority_queue:
            cost, current_node, fuel_left, fuel_spent = heapq.heappop(priority_queue)

            # Verifica se o nó atual é o objetivo
            if current_node == goal:
                # Reconstruir o caminho a partir dos pais
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = parent[current_node]
                path.reverse()
                return path, cost, fuel_spent

            if current_node not in visited:
                visited.add(current_node)

                for neighbor in self.graph.neighbors(current_node):
                    edge_data = self.graph.get_edge_data(current_node, neighbor)
                    if edge_data.get('closed', False):  # Ignora estradas fechadas
                        continue

                    edge_cost = edge_data.get('weight', 1)  # Distância da estrada
                    fuel_needed = edge_cost * vehicle.fuel_efficiency

                    # Se o combustível não for suficiente
                    if fuel_left < fuel_needed:
                        need_to_fuel = True
                        continue

                    # Calcular o custo acumulado para o vizinho
                    new_cost = cost + edge_cost

                    # Adicionar o vizinho à fila de prioridade com o novo custo
                    if neighbor not in visited:
                        heapq.heappush(priority_queue, (new_cost, neighbor, fuel_left - fuel_needed, fuel_spent + fuel_needed))
                        parent[neighbor] = current_node

        if need_to_fuel: 
            return self.find_nearest_supply(start, vehicle)
        return None, float('inf'), float('inf')  # Nenhum caminho encontrado
        
    def find_nearest_supply(self, node, vehicle):
        """
        Encontra a zona de supply mais próxima dentro do alcance do combustível restante.

        :param node: Nó de início.
        :param vehicle: Veículo utilizado na busca.
        :return: (caminho até a zona de supply, custo para alcançá-la, combustível total gasto) ou (None, infinito, infinito) se não for possível.
        """
        visited = set()
        queue = [(0, node, vehicle.fuel_capacity, 0)]  # (custo acumulado, nó atual, combustível restante, combustível gasto)
        parent = {node: None}  # Dicionário para reconstruir o caminho

        while queue:
            cost, current_node, remaining_fuel, fuel_spent = heapq.heappop(queue)

            if current_node in visited:
                continue
            visited.add(current_node)

            # Verifica se o nó atual é uma zona de supply
            if self.graph.nodes[current_node].get('zone_type') == 'supply':
                # Reconstruir o caminho
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = parent[current_node]
                path.reverse()
                return path, cost, fuel_spent

            for neighbor in self.graph.neighbors(current_node):
                edge_data = self.graph.get_edge_data(current_node, neighbor)
                if edge_data.get('closed', False):  # Se a estrada estiver fechada
                        continue
                
                edge_cost = edge_data.get('weight', 1)
                fuel_needed = edge_cost * vehicle.fuel_efficiency

                # Verifica se o combustível é suficiente para alcançar o vizinho, se não ignora vizinho
                if remaining_fuel >= fuel_needed and neighbor not in visited:
                    heapq.heappush(queue, (cost + edge_cost, neighbor, remaining_fuel - fuel_needed, fuel_spent + fuel_needed))
                    parent[neighbor] = current_node

        return None, float('inf'), float('inf')  # Nenhuma zona de supply acessível
