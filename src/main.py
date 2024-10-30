from Graph import Graph
from Node import Node


def main():
    g = Graph()

    g.createTest1()
    

    option = -1
    while option != 0:
        print("1-Imprimir Grafo")
        print("2-Desenhar Grafo")
        print("3-Imprimir nodos de Grafo")
        print("4-Imprimir arestas de Grafo")

        print("0-Sair")

        option = int(input("introduza a sua opcao-> "))
        if option == 0:
            print("saindo.......")
        elif option == 1:
            print(g.m_graph)
            l = input("prima enter para continuar")
        elif option == 2:
            g.draw()
        elif option == 3:
            print(g.m_graph.keys())
            l = input("prima enter para continuar")
        elif option == 4:
            print(g.print_edges())
            l = input("prima enter para continuar")
    
        else:
            print("you didn't add anything")
            l = input("prima enter para continuar")


if __name__ == "__main__":
    main()
