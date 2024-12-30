from models.vehicle import Truck, Car, Helicopter  # Ajusta o caminho conforme a estrutura do teu projeto


class DFS:
    def __init__(self, graph):
        """
        Inicializa a classe DFS com o grafo.

        :param graph: Grafo representando o mapa.
        """
        self.graph = graph

    def search(self, start, goal):
        """
        Realiza uma busca em profundidade (DFS) no grafo, considerando veículos, acessibilidade,
        e carga necessária.

        :param start: Nó inicial (zona de suporte).
        :param goal: Nó objetivo (zona que precisa de ajuda).
        :return: Caminho do nó inicial ao objetivo, lista de veículos necessários e custo.
        """
        visited = set()
        stack = [[start]]
        population_needed = self.graph.nodes[goal]["population"]
        vehicles = self.graph.nodes[start]["vehicles"]

        # Veículos disponíveis organizados por tipo
        vehicle_list = self._initialize_vehicles(vehicles)

        while stack:
            path = stack.pop()
            node = path[-1]

            if node == goal:
                # Encontrar os veículos necessários
                vehicle_plan, total_cost = self._allocate_vehicles(vehicle_list, population_needed, path)
                if vehicle_plan:
                    return path, vehicle_plan, total_cost
                continue

            if node not in visited:
                visited.add(node)
                for neighbor in self.graph.neighbors(node):
                    if self._can_access_zone(vehicle_list, neighbor):
                        new_path = list(path)
                        new_path.append(neighbor)
                        stack.append(new_path)
        return None

    def _initialize_vehicles(self, vehicles):
        """
        Inicializa os veículos disponíveis na zona inicial.

        :param vehicles: Lista de veículos na zona inicial.
        :return: Dicionário de veículos organizados por tipo.
        """
        vehicle_classes = {"truck": Truck, "car": Car, "helicopter": Helicopter}
        vehicle_list = []
        for vehicle in vehicles:
            vehicle_type = vehicle["type"]
            vehicle_quantity = vehicle["quantity"]
            vehicle_class = vehicle_classes[vehicle_type]
            for _ in range(vehicle_quantity):
                vehicle_list.append(vehicle_class(vehicle["id"]))
        return vehicle_list

    def _can_access_zone(self, vehicles, zone):
        """
        Verifica se há algum veículo capaz de acessar a zona.

        :param vehicles: Lista de veículos disponíveis.
        :param zone: ID da zona a verificar.
        :return: True se algum veículo pode acessar a zona, False caso contrário.
        """
        zone_accessibility = self.graph.nodes[zone]["accessibility"]
        return any(vehicle.id.lower() in zone_accessibility for vehicle in vehicles)

    def _allocate_vehicles(self, vehicles, population_needed, path):
        """
        Aloca veículos para transportar os mantimentos necessários, considerando apenas a distância percorrida.

        :param vehicles: Lista de veículos disponíveis.
        :param population_needed: Mantimentos necessários.
        :param path: Caminho a percorrer.
        :return: Lista de veículos alocados e custo total (distância).
        """
        allocated_vehicles = []
        total_distance = sum(self.graph.get_edge_data(path[i], path[i + 1]).get("weight", 0) for i in range(len(path) - 1))

        for vehicle in vehicles:
            if population_needed <= 0:
                break

            # Verificar se o veículo tem combustível suficiente para a rota
            if total_distance > vehicle.range:
                continue  # Ignorar veículos incapazes de completar a viagem

            # Alocar veículo
            if vehicle.capacity <= population_needed:
                allocated_vehicles.append(vehicle)
                population_needed -= vehicle.capacity

        if population_needed > 0:
            return None, None  # Não foi possível atender à demanda
        return allocated_vehicles, total_distance



    def _calculate_path_cost(self, path, vehicle):
        """
        Calcula o custo total do percurso para um veículo.

        :param path: Caminho percorrido.
        :param vehicle: Veículo utilizado.
        :return: Custo total (baseado na distância).
        """
        total_distance = 0
        for i in range(len(path) - 1):
            edge_data = self.graph.get_edge_data(path[i], path[i + 1])
            if edge_data:
                total_distance += edge_data.get("weight", 0)
        # Multiplicar pela eficiência do combustível
        return total_distance * vehicle.fuel_efficiency
