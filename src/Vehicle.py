

class Vehicle:
    def __init__(self, capacity, fuel_capacity, fuel_consumption, speed, location, load):
        self.capacity = capacity
        self.fuel_capacity = fuel_capacity
        self.fuel_consumption = fuel_consumption
        self.speed = speed
        self.location = location
        self.fuel_level = fuel_capacity
        self.load = capacity

    # Change location removing fuel
    def move(self, destination, distance, quantity):
        
        fuel_needed = distance * self.fuel_consumption

        if fuel_needed > self.fuel_level or self.load < quantity: # Not sufficient fuel
            return False

        self.fuel_level -= fuel_needed
        self.location = destination
        
        return True


    # Load
    def load_cargo(self, quantity):
        if self.load + quantity > self.capacity:
            return False
        
        self.load += quantity
        return True

    # Unload
    def unload_cargo(self, quantity):
        if self.load < quantity:
            self.load = 0
            return (quantity - self.load)
        
        self.load = self.load - quantity
        return 0


class Car(Vehicle):
    def __init__(self, location):
        super().__init__(capacity=500, fuel_capacity=100, fuel_consumption=0.2, speed=60, location=location)

class Helicopter(Vehicle):
    def __init__(self, location):
        super().__init__(capacity=200, fuel_capacity=75, fuel_consumption=0.5, speed=150, location=location)

class Truck(Vehicle):
    def __init__(self, location):
        super().__init__(capacity=1000, fuel_capacity=300, fuel_consumption=0.3, speed=40, location=location)
