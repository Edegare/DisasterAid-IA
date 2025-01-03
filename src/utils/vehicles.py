# utils/vehicles.py

from itertools import combinations_with_replacement

def calculate_vehicle_combination(population, vehicles):
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
