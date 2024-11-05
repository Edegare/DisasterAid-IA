from typing import Dict

from Projeto.IA.src.Weather import Weather


class Place:
    _id_counter = 1

    def __init__(self, x=None, y=None, id=None):
        if id is None:
            self.id: int = Place._id_counter  
            Place._id_counter += 1  
        else:
            self.id = id
        self.x = x
        self.y = y
        self.needs = {}
        self.weather: Weather = Weather.randomize()

    
    def __repr__(self):

        return f"Place(ID: {str(self.id)}, Coordinates: ({self.x}, {self.y}), Weather: {self.weather}, Needs: {self.needs})"

    def get_id(self):
        """Get id of the place"""
        return self.id
    
    def add_product(self, product, quantity):
        """Add a product and its quantity to the list of needs."""
        if product in self.needs:
            self.needs[product] += quantity  
        else:
            self.needs[product] = quantity 

    def remove_product(self, product, quantity):
        """Decrement quantity of a product or remove if quantity equals 0"""
        
        if product in self.needs:
            if self.needs[product] <= quantity:
                q = quantity - self.needs[product]
                del self.needs[product]
                return q 
            else : 
                q = self.needs[product] - quantity
                self.needs[product] = q 
                return 0 
        else: 
            return -1

    def get_weather(self) -> Weather:
        """Get the weather of the place"""
        return self.weather
