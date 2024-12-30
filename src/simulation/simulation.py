from datetime import datetime
import json
from search.dfs import DFS

class Simulation:
    def __init__(self, graph, algorithm, support_zones):
        """
        Inicializa a simulação.

        :param graph: Grafo com as zonas e conexões.
        :param algorithm: Algoritmo escolhido (string).
        :param support_zones: Lista de zonas de suporte.
        """
        self.graph = graph
        self.algorithm = algorithm
        self.support_zones = support_zones
        self.start_time = datetime.now()
        self.supply_zones = []  # Será preenchida no método start
        self.normal_zones = []  # Será preenchida no método start
        self.transport_logs = []  # Para guardar os dados de transporte

    def start(self):
        """
        Inicia a simulação.
        """
        # Obter supply zones
        self.supply_zones = [
            node for node, attrs in self.graph.nodes(data=True)
            if attrs.get('zone_type') == "supply"
        ]

        # Obter normal zones (zonas que precisam de ajuda)
        self.normal_zones = [
            node for node, attrs in self.graph.nodes(data=True)
            if attrs.get('zone_type') == "normal"
        ]

        # Exibir os resultados iniciais
        print(f"Simulação iniciada às {self.start_time}")
        print(f"Zonas de suporte: {self.support_zones}")
        print(f"Zonas de supply: {self.supply_zones}")
        print(f"Zonas a ajudar (normal): {self.normal_zones}")

        self.organize_zones_by_urgency()
        self.find_paths_for_normal_zones()
        self.save_simulation_results()

    def organize_zones_by_urgency(self):
        """
        Organiza as zonas normais por ordem de urgência, considerando prioridade e tempo crítico.
        """

        def calculate_urgency(zone_id):
            """
            Calcula o valor de urgência de uma zona com base na prioridade e tempo crítico.
            """
            zone = self.graph.nodes[zone_id]
            priority = zone.get('priority', 0)

            # Calcular o tempo restante em horas
            critical_time_str = zone.get('critical_time')
            if critical_time_str and critical_time_str != "0":
                critical_time = datetime.strptime(critical_time_str, "%Y-%m-%d %H:%M:%S")
                time_remaining = max(0, (critical_time - self.start_time).total_seconds() / 3600)  # Em horas
            else:
                time_remaining = float('inf')  # Sem tempo crítico, menos urgente

            # Fórmula de urgência
            urgency = (priority * 10) - (time_remaining / 2)
            
            # Garantir valores positivos e arredondar
            return max(0, int(urgency))

        # Ordenar as zonas normais pela urgência (decrescente)
        self.normal_zones.sort(key=calculate_urgency, reverse=True)

        # Exibir a lista organizada
        print("Zonas organizadas por urgência:")
        for zone_id in self.normal_zones:
            urgency = calculate_urgency(zone_id)
            print(f"Zona: {zone_id}, Urgência: {urgency}")

    def find_paths_for_normal_zones(self):
        """
        Para cada zona normal, encontra o melhor caminho através das zonas de suporte usando o algoritmo selecionado
        e organiza o transporte dos mantimentos.
        """
        for normal_zone in self.normal_zones:
            print(f"Encontrando caminhos para a zona {normal_zone}...")

            best_path = None
            best_cost = float('inf')
            best_vehicles = None

            for support_zone in self.support_zones:
                path, vehicles = self.find_path(normal_zone, support_zone)

                if path:
                    path_cost = self.calculate_path_cost(path)
                    print(f"Caminho encontrado de {support_zone} para {normal_zone}: {path} com custo {path_cost}")

                    if path_cost < best_cost:
                        best_path = path
                        best_cost = path_cost
                        best_vehicles = vehicles

            if best_path and best_vehicles:
                print(f"Melhor caminho para {normal_zone}: {best_path} com custo {best_cost}")
                self.send_supplies(normal_zone, best_path, best_vehicles, best_cost)
            else:
                print(f"Não foi possível encontrar um caminho para {normal_zone}")

    def find_path(self, start, goal):
        """
        Determina o caminho entre dois nós usando o algoritmo selecionado (estrutura básica).
        Retorna o caminho encontrado e uma lista de veículos necessários.
        """
        if self.algorithm == "BFS":
            return self._bfs(start, goal), []
        elif self.algorithm == "DFS":
            return self._dfs(start, goal), []
        elif self.algorithm == "Greedy":
            return self._greedy(start, goal), []
        elif self.algorithm == "AStar":
            return self._astar(start, goal), []
        else:
            raise ValueError(f"Algoritmo {self.algorithm} não reconhecido.")

    def send_supplies(self, destination, path, vehicles, cost):
        """
        Realiza o envio de mantimentos para a zona normal especificada.

        :param destination: Zona de destino.
        :param path: Caminho usado para a entrega.
        :param vehicles: Lista de veículos utilizados.
        :param cost: Custo do transporte (em distância).
        """
        if path and path[0] in self.support_zones:
            self.reduce_vehicles_in_support_zone(path[0], vehicles)

        arrival_time = self.calculate_arrival_time(path, vehicles)
        self.transport_logs.append({
            "from": path[0],
            "to": destination,
            "path": path,
            "vehicles": vehicles,
            "cost": cost,
            "arrival_time": arrival_time,
            "stops": [zone for zone in path if zone in self.supply_zones]
        })

    def reduce_vehicles_in_support_zone(self, support_zone, vehicles):
        """
        Reduz o número de veículos disponíveis na zona de suporte escolhida.

        :param support_zone: Zona de suporte utilizada.
        :param vehicles: Veículos utilizados.
        """
        support_data = self.graph.nodes[support_zone].get('vehicles', [])
        for vehicle in vehicles:
            for v in support_data:
                if v['id'] == vehicle['id'] and v['quantity'] > 0:
                    v['quantity'] -= 1

    def calculate_arrival_time(self, path, vehicles):
        """
        Calcula o tempo de chegada ao destino com base na velocidade do veículo e na distância total.
        """
        total_distance = self.calculate_path_cost(path)
        average_speed = min(v['speed'] for v in vehicles)
        travel_time = total_distance / average_speed  # Tempo em horas
        return self.start_time + timedelta(hours=travel_time)

    def calculate_path_cost(self, path):
        """
        Calcula o custo total de um caminho (Placeholder).
        """
        return sum(self.graph.get_edge_data(path[i], path[i + 1])['weight'] for i in range(len(path) - 1))

    def save_simulation_results(self):
        """
        Guarda os resultados da simulação num ficheiro JSON.
        """
        with open("simulation_results.json", "w") as file:
            json.dump(self.transport_logs, file, indent=4)
        print("Resultados da simulação guardados em 'simulation_results.json'.")

    
