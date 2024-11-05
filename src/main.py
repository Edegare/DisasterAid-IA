import os
import osmnx as ox
import networkx as nx
import pickle

from Projeto.IA.src.Place import Place
from Projeto.IA.src.Graph import Graph


def load_or_create_graph():
    file_path = "road_network_gualtar.gpickle"
    
    if os.path.exists(file_path):
        print("Graph file found. Loading the graph from file...")
        with open(file_path, "rb") as f:
            G = pickle.load(f)
    else:
        print("Graph file not found. Creating a new graph for Gualtar...")
        G = ox.graph_from_place("Gualtar, Portugal", network_type="drive")

        # Assign sequential IDs to each node
        id = 1
        for node, data in G.nodes(data=True):
            data["id"] = id  
            id += 1  
        
        # Save the graph with custom node IDs
        with open(file_path, "wb") as f:
            pickle.dump(G, f)
        print("Graph created and saved with custom IDs.")

    return G


def main():
    # Load the OSMnx graph
    G = load_or_create_graph()
    
    # Create custom graph from OSMnx graph
    custom_graph = Graph(G)
    print(custom_graph)

    # Example: Get all places
    places = custom_graph.get_places()
    print(f"Total places: {len(places)}")
    print("Sample place:", places[len(places) // 2]) 

    # Example: Get all roads
    roads = custom_graph.get_roads()
    print(f"Total roads: {len(roads)}")
    print("Sample road:", roads[len(roads) // 2])  

    # Example: Find roads from a specific place
    sample_place: Place = places[len(places) // 3]
    print(f"Roads from {sample_place.get_id()}: {custom_graph.find_roads_from_place(sample_place)}")

    # Visualize the graph
    print("Visualizing the graph...")
    ox.plot_graph(custom_graph.ox, node_size=10, edge_linewidth=1)

if __name__ == "__main__":
    main()