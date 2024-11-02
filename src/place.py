from typing import Dict

from weather import Weather


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
        self.weather: Weather = Weather.randomize()

    
    def __repr__(self):
        return f"Place(ID: {str(self.id)}, Coordinates: ({self.x}, {self.y}), Weather: {self.weather})"

    def get_id(self):
        return self.id
    
    
    def get_weather(self) -> Weather:
        return self.weather
