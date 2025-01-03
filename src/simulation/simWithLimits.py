# simulation/simWithLimits.py

from search import UCS
from search import GreedyBestFirstSearch
from search import AStar
from search import DFS
from search import BFS
from models import Helicopter, Truck, Car, Vehicle
from utils import writeToJson

from datetime import datetime, timedelta
from collections import defaultdict
from simulation import Simulation

import json

class SimulationWithLimits:
    def __init__(self, graph, algorithm_type):
        self.graph = graph
        self.algorithm_type = algorithm_type
        self.support_zones = []
        self.normal_zones = []
        self.start_time = datetime.now()
        self.current_time = self.start_time  # Tempo atual simulado
        self.vehicle_refill_time = timedelta(hours=2)  # Tempo para reabastecer veículos
        self.vehicle_availability = defaultdict(list)

    def initialize_zones(self):
        """
        Inicializa as zonas de suporte e normais e popula os veículos disponíveis.
        """
        self.support_zones = [
            node for node, attrs in self.graph.nodes(data=True)
            if attrs.get('zone_type') == "support"
        ]
        self.normal_zones = [
            node for node, attrs in self.graph.nodes(data=True)
            if attrs.get('zone_type') == "normal"
        ]
        self.organize_zones_by_urgency()
        
        for zone in self.support_zones:
            vehicles_data = self.graph.nodes[zone].get('vehicles', [])
            for vehicle_data in vehicles_data:
                for _ in range(vehicle_data['available']):
                    if vehicle_data['type'] == 'truck':
                        vehicle = Truck(vehicle_data['id'])
                    elif vehicle_data['type'] == 'car':
                        vehicle = Car(vehicle_data['id'])
                    elif vehicle_data['type'] == 'helicopter':
                        vehicle = Helicopter(vehicle_data['id'])
                    else:
                        continue
                    # Adicionar atributo de disponibilidade inicial
                    vehicle.initial_available = vehicle_data['available']
                    self.vehicle_availability[zone].append(vehicle)

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

    
    
    def replenish_vehicles(self):
        """
        Reabastece os veículos e restaura a disponibilidade inicial em todas as zonas de suporte.
        """
        for zone, vehicles in self.vehicle_availability.items():
            initial_counts = defaultdict(int)

            # Contar veículos disponíveis atualmente
            for vehicle in vehicles:
                initial_counts[vehicle.id] += 1

            # Restaurar combustível e garantir que o número inicial esteja presente
            for vehicle in vehicles:
                vehicle.current_fuel = vehicle.fuel_capacity  # Reabastece o tanque

            # Garantir que os valores iniciais sejam repostos
            zone_data = self.graph.nodes[zone].get('vehicles', [])
            for vehicle_data in zone_data:
                vehicle_type = vehicle_data['id']
                initial_available = vehicle_data['available']
                while initial_counts[vehicle_type] < initial_available:
                    if vehicle_data['type'] == 'truck':
                        new_vehicle = Truck(vehicle_type)
                    elif vehicle_data['type'] == 'car':
                        new_vehicle = Car(vehicle_type)
                    elif vehicle_data['type'] == 'helicopter':
                        new_vehicle = Helicopter(vehicle_type)
                    else:
                        continue
                    new_vehicle.current_fuel = new_vehicle.fuel_capacity
                    vehicles.append(new_vehicle)
                    initial_counts[vehicle_type] += 1

    def calculate_best_paths(self):
        """
        Calcula os melhores caminhos de cada zona de suporte para as zonas normais.
        """
        algorithms = {
            "DFS": DFS(self.graph),
            "BFS": BFS(self.graph),
            "UCS": UCS(self.graph),
            "Greedy": GreedyBestFirstSearch(self.graph),
            "AStar": AStar(self.graph)
        }
        algorithm = algorithms[self.algorithm_type]

        completed_zones = []
        best_paths = {}

        while len(completed_zones) < len(self.normal_zones):
            max_delivery_time = timedelta(0)  # Armazena o maior tempo de entrega deste ciclo

            for normal_zone in self.normal_zones:
                if normal_zone in completed_zones:
                    continue

                best_path = None
                best_cost = float('inf')
                best_vehicles = []

                for support_zone in self.support_zones:
                    vehicles = self.vehicle_availability[support_zone]
                    if not vehicles:
                        continue

                    path, cost, vehicles_used = algorithm.search(support_zone, normal_zone)
                    if cost < best_cost and self.check_vehicle_availability(vehicles, vehicles_used):
                        best_path = path
                        best_cost = cost
                        best_vehicles = vehicles_used

                if best_path:
                    # Atualizar disponibilidade e verificar sucesso
                    if not self.update_vehicle_availability(support_zone, best_vehicles):
                        continue  # Se veículos insuficientes, passa para a próxima iteração
                    delivery_time = self.calculate_delivery_time(best_cost, best_vehicles)
                    max_delivery_time = max(max_delivery_time, delivery_time - self.current_time)

                    best_paths[normal_zone] = {
                        "path": best_path,
                        "cost": best_cost,
                        "vehicles": best_vehicles
                    }
                    completed_zones.append(normal_zone)

            # Incrementar o tempo atual com o maior tempo de entrega do ciclo
            self.current_time += max_delivery_time
            self.replenish_vehicles()

        return best_paths
    
    def calculate_delivery_time(self, distance, vehicles):
        """
        Calcula o tempo estimado de entrega com base na velocidade do veículo mais lento.
        """
        vehicle_mapping = {
            'truck': Truck,
            'car': Car,
            'helicopter': Helicopter
        }

        # Lista para armazenar velocidades de veículos após a criação das instâncias
        vehicle_speeds = []

        for vehicle_data in vehicles:
            vehicle_type = vehicle_data['id']
            quantity = vehicle_data.get('quantity', 1)  # Quantidade de veículos

            # Criar instâncias dos veículos
            if vehicle_type in vehicle_mapping:
                for _ in range(quantity):
                    vehicle_instance = vehicle_mapping[vehicle_type](vehicle_type)
                    vehicle_speeds.append(vehicle_instance.speed)

        if not vehicle_speeds:
            raise ValueError("Nenhum veículo válido fornecido para cálculo do tempo de entrega.")

        # Encontrar a menor velocidade entre os veículos
        slowest_speed = min(vehicle_speeds)

        # Calcular o tempo de viagem com base na menor velocidade
        travel_time_hours = distance / slowest_speed
        travel_time = timedelta(hours=travel_time_hours)

        # Retornar o tempo estimado de entrega
        return self.current_time + travel_time
    
    def check_vehicle_availability(self, available_vehicles, required_vehicles):
        """
        Verifica se os veículos necessários estão disponíveis na zona de suporte.
        """
        available_counts = defaultdict(int)
        for vehicle in available_vehicles:
            # Suporta tanto dicionários quanto instâncias de Vehicle
            vehicle_id = vehicle.id if isinstance(vehicle, Vehicle) else vehicle['id']
            available_counts[vehicle_id] += vehicle.get('available', 0) if isinstance(vehicle, dict) else vehicle.available

        for vehicle in required_vehicles:
            # Suporta tanto dicionários quanto instâncias de Vehicle
            vehicle_id = vehicle.id if isinstance(vehicle, Vehicle) else vehicle['id']
            required_quantity = vehicle.get('quantity', 1) if isinstance(vehicle, dict) else 1
            if available_counts[vehicle_id] < required_quantity:
                return False
            
        return True
    
    def update_vehicle_availability(self, support_zone, used_vehicles):
        """
        Atualiza a disponibilidade dos veículos após um envio.
        Retorna False se os veículos forem insuficientes, True caso contrário.
        """
        for used_vehicle in used_vehicles:
            vehicle_id = used_vehicle.id if isinstance(used_vehicle, Vehicle) else used_vehicle.get('id')
            required_quantity = used_vehicle.get('quantity', 1) if isinstance(used_vehicle, dict) else 1
            used_count = 0

            # Verificar veículos disponíveis na zona de suporte
            for vehicle in list(self.vehicle_availability[support_zone]):
                if vehicle.id == vehicle_id:
                    self.vehicle_availability[support_zone].remove(vehicle)
                    used_count += 1
                    if used_count == required_quantity:
                        break

            # Se não conseguir encontrar veículos suficientes
            if used_count < required_quantity:
                return False
        return True

    def start_simulation(self):
        """
        Inicia a simulação.
        """
        self.initialize_zones()
        results = self.calculate_best_paths()
        writeToJson(results, self.graph, self.algorithm_type, 1)
