def print_graph(graph):
    """
    Imprime os nós e arestas do grafo com seus atributos.
    """
    print("Nós:")
    for node, data in graph.nodes(data=True):
        print(f"  {node}: {data}")
    
    print("\nArestas:")
    for u, v, data in graph.edges(data=True):
        print(f"  ({u}, {v}): {data}")