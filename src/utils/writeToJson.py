# utils/writeToJson.py

from models import Truck, Car, Helicopter

from datetime import datetime, timedelta
import os
import json
import math

def writeToJson(best_paths, graph, algorithm_name, type):
    """
    Escreve os resultados dos melhores caminhos num ficheiro JSON com base no algoritmo escolhido.

    :param best_paths: Dicionário contendo os melhores caminhos calculados.
    :param graph: Grafo representando o mapa.
    :param algorithm_name: Nome do algoritmo utilizado.
    :param type: Define o tipo de simulação. 0 para normalSim, 1 para limitSim.
    """
    results = []

    for end_node, path_data in best_paths.items():
        start_node = path_data['path'][0]
        path = path_data['path']
        population = graph.nodes[end_node].get('population', 0)
        unTruncDistance = path_data['cost']
        distance = math.trunc(unTruncDistance * 100) / 100
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

    # Determinar o diretório de saída
    output_dir = "results/normalSim" if type == 0 else "results/limitSim"
    os.makedirs(output_dir, exist_ok=True)

    # Determinar o nome do ficheiro com base no algoritmo
    file_name = os.path.join(output_dir, f"results_{algorithm_name.lower()}.json")

    # Escrever no ficheiro JSON
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"Resultados escritos no ficheiro '{file_name}'.")