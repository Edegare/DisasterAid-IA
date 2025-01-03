# simulation/simulation.py

from search import DFS
from search import BFS
from search import UCS
from search import GreedyBestFirstSearch
from search import AStar
from models import Truck, Car, Helicopter

from datetime import datetime, timedelta

import json

class Simulation:
    def __init__(self, graph, algorithm_type):
        """
        Inicializa a simulação.

        :param graph: Grafo gerado a partir dos dados JSON.
        :param algorithm_type: String indicando o tipo de algoritmo escolhido.
        """
        self.graph = graph
        self.algorithm_type = algorithm_type
        self.support_zones= []
        self.supply_zones = []
        self.normal_zones = []
        self.start_time = datetime.now()

    def start(self):
        """
        Executa a lógica principal da simulação.
        """

        # Obter support zones
        self.support_zones = [
            node for node, attrs in self.graph.nodes(data=True)
            if attrs.get('zone_type') == "support"
        ]

        print("Nós no grafo:", list(self.graph.nodes))

        print("Zonas support:", self.support_zones)

        # Obter supply zones - ainda não serve para nada
        self.supply_zones = [
            node for node, attrs in self.graph.nodes(data=True)
            if attrs.get('zone_type') == "supply"
        ]

        # Obter normal zones
        self.normal_zones = [
            node for node, attrs in self.graph.nodes(data=True)
            if attrs.get('zone_type') == "normal"
        ]

        print("Zonas normais antes de organizar por urgência:", self.normal_zones)
        self.organize_zones_by_urgency()
        print("Zonas normais organizadas por urgência:", self.normal_zones)
        print("Nós no grafo:", list(self.graph.nodes))
        print("Zonas support:", self.support_zones)


        # Calcular o melhor caminho para cada zona normal
        best_paths = self.calculate_best_paths()
        """ 
        for normal_zone, path_data in best_paths.items():
            vehicles = path_data.get("vehicles", [])
            print(f"Melhor caminho para {normal_zone}: {path_data['path']} com custo {path_data['cost']}")
            if vehicles:
                vehicle_str = ", ".join([f"{v['quantity']}x {v['id']}" for v in vehicles])
                print(f"Veículos utilizados: {vehicle_str}")
            else:
                print(f"Nenhum veículo necessário para {normal_zone}.")
        """

        self.write_results_to_json(best_paths, self.graph)



    def calculate_best_paths(self):
        """
        Calcula o melhor caminho de cada zona normal para uma zona de suporte.

        :return: Dicionário com os melhores caminhos, custos associados e veículos utilizados para cada zona normal.
        """
        algorithms = {
            "BFS": BFS(self.graph),
            "DFS": DFS(self.graph),
            "UCS": UCS(self.graph),
            "Greedy": GreedyBestFirstSearch(self.graph),
            "A*": AStar(self.graph)
        }

        if self.algorithm_type not in algorithms or algorithms[self.algorithm_type] is None:
            raise ValueError("Algoritmo inválido ou não implementado.")

        algorithm = algorithms[self.algorithm_type]

        best_paths = {}

        for normal_zone in self.normal_zones:
            best_path = None
            best_cost = float('inf')
            best_vehicles = []

            # Obter o nó do grafo correspondente à zona normal
            normal_node = self.graph.nodes.get(normal_zone)
            if not normal_node:
                print(f"Erro: A zona normal {normal_zone} não foi encontrada no grafo.")
                continue

            for support_zone in self.support_zones:
                # Obter o nó do grafo correspondente à zona de suporte
                support_node = self.graph.nodes.get(support_zone)
                if not support_node:
                    print(f"Erro: A zona de suporte {support_zone} não foi encontrada no grafo.")
                    continue

                try:
                    print(f"Tentando caminho de {support_zone} para {normal_zone}")
                    path, cost, vehicles = algorithm.search(support_zone, normal_zone)
                    cost = round(cost, 2)
                    if cost < best_cost:
                        best_path = path
                        best_cost = cost
                        best_vehicles = vehicles
                except Exception as e:
                    print(f"Erro ao calcular caminho de {support_zone} para {normal_zone}: {e}")

            if best_path is not None:
                best_paths[normal_zone] = {
                    "path": best_path,
                    "cost": best_cost,
                    "vehicles": [{"id": v["id"], "quantity": v["quantity"]} for v in best_vehicles]
                }


        return best_paths


    
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
            urgency = (priority * 100) + max(0, 1000 / (time_remaining + 1))
            
            # Garantir valores positivos e arredondar
            return max(0, int(urgency))

        # Ordenar as zonas normais pela urgência (decrescente)
        self.normal_zones.sort(key=calculate_urgency, reverse=True)


    def write_results_to_json(self, best_paths, graph):
        """
        Escreve os resultados dos melhores caminhos num ficheiro JSON com base no algoritmo escolhido.

        O ficheiro terá o nome formatado como `results_<algorithm>.json`, onde <algorithm> é o tipo do algoritmo utilizado.

        :param best_paths: Dicionário contendo os melhores caminhos calculados.
        :param graph: Grafo representando o mapa.
        """
        
        results = []

        for end_node, path_data in best_paths.items():
            start_node = path_data['path'][0]
            path = path_data['path']
            population = graph.nodes[end_node].get('population', 0)
            distance = path_data['cost']
            vehicles = path_data.get('vehicles', [])
            critical_time = graph.nodes[end_node].get('critical_time', "N/A")

            vehicle_details = []
            arrival_times = []

            for vehicle_data in vehicles:
                vehicle_type = vehicle_data['id']
                quantity = vehicle_data['quantity']

                # Obter atributos do veículo
                if vehicle_type == 'truck':
                    vehicle = Truck(vehicle_type)
                elif vehicle_type == 'car':
                    vehicle = Car(vehicle_type)
                elif vehicle_type == 'helicopter':
                    vehicle = Helicopter(vehicle_type)
                else:
                    continue

                refuels = []
                current_range = vehicle.range
                travel_details = []

                for i in range(len(path) - 1):
                    current_node = path[i]
                    next_node = path[i + 1]

                    edge_data = graph.get_edge_data(current_node, next_node, default={})
                    edge_distance = edge_data.get('weight', float('inf'))
                    weather = edge_data.get('weather', "Sol")
                    weather_impact = {
                        "Sol": 1.0,
                        "Chuva": 0.85,
                        "Nevoeiro": 0.7,
                        "Neve/Gelo": 0.5
                    }

                    adjusted_speed = vehicle.speed * weather_impact[weather]
                    travel_time = edge_distance / adjusted_speed

                    travel_details.append({
                        'from': current_node,
                        'to': next_node,
                        'weather': weather,
                        'distance': edge_distance,
                        'adjusted_speed': round(adjusted_speed, 2),
                        'travel_time_hours': round(travel_time, 2)
                    })

                    if current_range < edge_distance:
                        refuels.append(current_node)
                        current_range = vehicle.range

                    current_range -= edge_distance

                travel_time_total = sum(detail['travel_time_hours'] for detail in travel_details)
                arrival_time = datetime.now() + timedelta(hours=travel_time_total)
                arrival_times.append(arrival_time)

                vehicle_details.append({
                    'type': vehicle_type,
                    'quantity': quantity,
                    'refuels': refuels,
                    'travel_details': travel_details,
                    'total_travel_time': round(travel_time_total, 2),
                    'arrival_time': arrival_time.strftime("%Y-%m-%d %H:%M:%S")
                })

            # Determinar o tempo final de chegada (o maior tempo entre os veículos)
            final_arrival_time = max(arrival_times) if arrival_times else None

            # Converter o caminho para o formato "A -> B -> C"
            formatted_path = " -> ".join(path)

            # Adicionar os resultados
            results.append({
                'start_node': start_node,
                'end_node': end_node,
                'population': population,
                'distance': distance,
                'best_path': formatted_path,
                'vehicles': vehicle_details,
                'critical_time': critical_time,
                'final_arrival_time': final_arrival_time.strftime("%Y-%m-%d %H:%M:%S") if final_arrival_time else "N/A"
            })

        # Determinar o nome do ficheiro com base no algoritmo
        algorithm_name = self.algorithm_type.lower()
        file_name = f"results_{algorithm_name}.json"

        # Escrever no ficheiro JSON
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        print(f"Resultados escritos no ficheiro '{file_name}'.")