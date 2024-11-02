import osmnx as ox
import networkx as nx

from place import Place
from road import Road


class Graph:
    def __init__(self, ox_graph):
        """
        Initialize the Graph from an existing OSMnx graph.
        
        Parameters:
        - ox_graph: The graph created using OSMnx.
        """
        
        self.places = {}  # Dictionary to hold Place instances with custom IDs as keys
        self.roads = {}   # Dictionary to hold lists of Road instances for each Place ID
        self.ox= ox_graph


        # Create Place objects for each node in the OSMnx graph using custom IDs
        for node_id, node_data in ox_graph.nodes(data=True):
            x = node_data.get("x", None)
            y = node_data.get("y", None)
            custom_id = node_data["id"] 
            place = Place(x=x, y=y, id=custom_id)
            self.places[custom_id] = place
            self.roads[custom_id] = []  

        # Create Road objects for each edge in the OSMnx graph
        for u, v, data in ox_graph.edges(data=True):
            length = data.get("length", 0)
            src_id = ox_graph.nodes[u]["id"]
            dest_id = ox_graph.nodes[v]["id"]
            road = Road(src=self.places[src_id], to=self.places[dest_id], length=length)
            self.roads[src_id].append(road) 

    def __repr__(self):
        return f"Graph with {len(self.places)} places and {sum(len(roads) for roads in self.roads.values())} roads."

    def get_places(self):
        return list(self.places.values())

    def get_roads(self):
        # Flatten the list of roads for all places into a single list
        return [road for roads in self.roads.values() for road in roads]

    def find_place_by_id(self, place_id):
        return self.places.get(place_id, None)

    def find_roads_from_place(self, place):
        """
        Returns a list of all roads that start from the given Place.
        """
        return self.roads.get(place.id, [])

    def find_roads_to_place(self, place):
        """
        Returns a list of all roads that end at the given Place.
        """
        return [road for roads in self.roads.values() for road in roads if road.get_destination() == place]
