import sys
import json
import matplotlib.pyplot as plt
from utils.graph import print_graph
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

    print("")
    option = -1
    while option != 0:
        
        print("== Sistema de Procura de Distribuição de Suprimentos ==")
        print("1. Desenhar Grafo")
        print("2. Imprimir nós e arestas do Grafo")
        print("3. Executar Algoritmos de Procura")
        print("4. Visualizar Resultados")
        print("0. Sair")
        option = int(input("Selecione uma opção: "))
        
        print("")

        if option == 0:
            print("Saindo...")
        elif option == 1: # Mostrar grafo
            map_generator.display_graph()

        elif option == 2: # Imprimir grafo
            print_graph(graph)
            input("Pressione Enter para continuar!")
            print("")

        elif option == 3: 
            # Menu de Algoritmos de procura
            optionSearch = -1
            while optionSearch != 0:

                # Solicitar o algoritmo ao utilizador
                print("Selecione o algoritmo de procura a utilizar:")
                print("1. BFS (Breadth-First Search)")
                print("2. DFS (Depth-First Search)")
                print("3. UCS (Uniform Cost Search)")
                print("4. Greedy Best-First Search")
                print("5. A* (A-Star)")
                print("0. Sair")

                algorithm_choice = input("Digite o número correspondente ao algoritmo: ")
                optionSearch = int(algorithm_choice)

                if optionSearch == 0:
                    print("Saindo do Menu de Procura...")
                
                else:
                    algorithm_types = {
                        "1": "BFS",
                        "2": "DFS",
                        "3": "UCS",
                        "4": "Greedy",
                        "5": "A*"
                    }

                    if algorithm_choice not in algorithm_types:
                        print("Opção inválida.")
                    
                    else: 
                        algorithm_type = algorithm_types[algorithm_choice]

                        simulation = Simulation(graph, algorithm_type)
                        simulation.start()
                print("")

        elif option == 4:
            # Menu de Algoritmos de procura
            algorithm_choice = -1
            while algorithm_choice != 0:

                # Solicitar o algoritmo ao utilizador
                print("Selecione o algoritmo para visualizar os resultados:")
                print("1. BFS (Breadth-First Search)")
                print("2. DFS (Depth-First Search)")
                print("3. UCS (Uniform Cost Search)")
                print("4. Greedy Best-First Search")
                print("5. A* (A-Star)")
                print("0. Sair")

                algorithm_choice = input("Digite o número correspondente ao algoritmo: ")

                if algorithm_choice == "0":
                    print("Saindo da visualização de resultados...")

                else:
                    algorithm_types = {
                        "1": "bfs",
                        "2": "dfs",
                        "3": "ucs",
                        "4": "greedy",
                        "5": "astar"
                    }

                    if algorithm_choice not in algorithm_types:
                        print("Opção inválida.")

                    else:
                        algorithm_name = algorithm_types[algorithm_choice]
                        file_name = f"results_{algorithm_name}.json"

                        try:
                            with open(file_name, 'r', encoding='utf-8') as file:
                                results = json.load(file)
                        except FileNotFoundError:
                            print(f"Erro: O ficheiro '{file_name}' não foi encontrado.")
                            continue

                        index = 0
                        while True:
                            result = results[index]
                            print(f"\nVisualizando Resultado {index + 1}/{len(results)}")
                            print(f"Start Node: {result['start_node']}")
                            print(f"End Node: {result['end_node']}")
                            print(f"Population: {result['population']}")
                            print(f"Distance: {result['distance']} km")
                            print(f"Best Path: {result['best_path']}")
                            print(f"Vehicles: {result['vehicles']}")
                            print(f"Critical Time: {result['critical_time']}")
                            print(f"Final Arrival Time: {result['final_arrival_time']}")

                            # Converter caminho do formato "A -> B -> C" para lista
                            path = result['best_path'].split(" -> ")

                            # Mostrar grafo com destaque no caminho
                            map_generator.display_graph(path=path)

                            # Navegação entre resultados
                            print("\nControles: 'a' para Anterior, 'd' para Próximo, '0' para Sair.")
                            control = input("Digite sua escolha: ").strip().lower()
                            if control == "0":
                                print("Saindo da visualização de resultados...")
                                break
                            elif control == "d":
                                index = (index + 1) % len(results)
                            elif control == "a":
                                index = (index - 1 + len(results)) % len(results)
                            else:
                                print("Comando inválido.")
                    print("")

        else:
             print("Opção inválida.")
             print("")

if __name__ == "__main__":
    main()
