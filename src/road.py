import random

from place import Place
from weather import Weather

import random

class Road:

    _id_counter = 1

    def __init__(self, src: Place, to: Place, length) -> None:
        self.id: int = Road._id_counter  
        Road._id_counter += 1  
        self.src = src
        self.to = to
        self.length = length
        self.open = True
        src_weather = src.get_weather()
        to_weather = to.get_weather()
        self.weather = random.choice([src_weather, to_weather])

    def __repr__(self):
        return (f"Road (ID: {str(self.id)}) from {self.src.id} to {self.to.id}, "
                f"Length: {self.length}, Open: {self.open}, Weather: {self.weather}\n")

    def get_destination(self):
        return self.to

    def get_source(self):
        return self.src

    def get_weather(self):
        return self.weather

