import sys
from utils.graph import print_graph
from map.mapGenerator import MapGenerator
from simulation.simulation import Simulation

def main():

    from geopy.distance import geodesic
        
        
    goal_coords = (46.6354, 32.6169)
    poltava = (49.5883, 34.5514)
    cherkassi = (49.4444, 32.0598)

    print("poltava: ")
    print(geodesic(poltava, goal_coords).kilometers)
    print("cherkassi: ")
    print(geodesic(cherkassi, goal_coords).kilometers)
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

        else:
             print("Opção inválida.")
             print("")

if __name__ == "__main__":
    main()
