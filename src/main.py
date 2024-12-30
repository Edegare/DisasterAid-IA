import os
from map.mapGenerator import MapGenerator
from simulation.simulation import Simulation 
from search.dfs import DFS

def print_result(result):
    if result:
        path, vehicle_plan, total_cost = result

        # Organizar veículos por tipo e quantidade
        vehicle_summary = {}
        for vehicle in vehicle_plan:
            vehicle_type = vehicle.id
            if vehicle_type in vehicle_summary:
                vehicle_summary[vehicle_type] += 1
            else:
                vehicle_summary[vehicle_type] = 1

        # Exibir resultados formatados
        print(f"Caminho: {' -> '.join(path)}")
        print("Veículos alocados:")
        for vehicle_type, count in vehicle_summary.items():
            print(f"  - {vehicle_type}: {count} unidades")
        print(f"Custo total: {total_cost:.2f}")
    else:
        print("Não foi possível encontrar um caminho viável.")

def main():
    # Obter o caminho do ficheiro JSON do mapa
    input_path = input("Insira o caminho para o ficheiro JSON do mapa: ").strip()

    if not os.path.exists(input_path):
        print("Caminho inválido. Certifique-se de que o ficheiro existe.")
        return

    # Gerar o mapa
    map_generator = MapGenerator(json_path=input_path)
    # Gerar o mapa e obter as zonas de suporte
    support_zones = map_generator.load_zones()
    map_generator.display_graph()
    print(f"Mapa gerado com sucesso! Zonas de suporte identificadas: {support_zones}")

    # Perguntar pelo algoritmo de procura
    print("Escolha o algoritmo:")
    print("1. BFS")
    print("2. DFS")
    print("3. UCS")
    print("4. Greedy")
    print("5. A*")
    algorithm_choice = input("Opção: ").strip()

    algorithms = {
        "1": "BFS",
        "2": "DFS",
        "3": "UCS",
        "4": "Greedy",
        "5": "AStar"
    }

    if algorithm_choice not in algorithms:
        print("Opção inválida.")
        return

    chosen_algorithm = algorithms[algorithm_choice]
    print(chosen_algorithm)

    # Inicializar a simulação
    print("Inicializando a simulação...")
    simulation = Simulation(graph=map_generator.graph, algorithm=chosen_algorithm, support_zones=support_zones)

    # Iniciar a simulação
    simulation.start()

    dfs = DFS(map_generator.graph)
    start = "Braga"
    goal = "Amares"
    result = dfs.search(start, goal)

    print_result(result)

if __name__ == "__main__":
    main()
