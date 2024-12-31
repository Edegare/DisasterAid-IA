import sys
from map.mapGenerator import MapGenerator
from simulation.simulation import Simulation

def main():
    # Obter o caminho do ficheiro JSON do mapa
    input_path = input("Insira o caminho para o ficheiro JSON do mapa: ").strip()

    # Inicializar o gerador de mapas
    print("Inicializando o gerador de mapas...")
    map_generator = MapGenerator(json_path=input_path)

    # Carregar as zonas e gerar o grafo
    print("Carregando zonas e gerando o grafo...")
    try:
        map_generator.load_zones()
    except FileNotFoundError:
        print(f"Erro: Ficheiro JSON não encontrado em {json_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao carregar o ficheiro JSON: {e}")
        sys.exit(1)

    # Exibir o grafo (opcional, apenas para validação inicial)
    map_generator.display_graph()

    # Obter informações úteis para debug
    graph = map_generator.graph

    # Solicitar o algoritmo ao utilizador
    print("Selecione o algoritmo de procura a utilizar:")
    print("1. BFS (Breadth-First Search)")
    print("2. DFS (Depth-First Search)")
    print("3. UCS (Uniform Cost Search)")
    print("4. Greedy Best-First Search")
    print("5. A* (A-Star)")

    algorithm_choice = input("Digite o número correspondente ao algoritmo: ")

    algorithm_types = {
        "1": "BFS",
        "2": "DFS",
        "3": "UCS",
        "4": "Greedy",
        "5": "A*"
    }

    if algorithm_choice not in algorithm_types:
        print("Opção inválida.")
        sys.exit(1)

    algorithm_type = algorithm_types[algorithm_choice]

    simulation = Simulation(graph, algorithm_type)
    simulation.start()

if __name__ == "__main__":
    main()
