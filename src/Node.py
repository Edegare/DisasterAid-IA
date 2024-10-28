# Class that define nodes (zones)
# Each node has an ID, Name, the number of needs, critic time and weather


class Node: 
    
        # Node (zone) in the graph.
        
        # Parameters:
        # - id: Unique identifier for the zone.
        # - name: Name of the zone.
        # - needs: Amount of assistance needed.
        # - time: Critical time for the zone.
        # - weather: Current weather conditions in the zone.


    def __init__(self, id, name, needs, time, weather):     
        self.m_id = id
        self.m_name = str(name)
        self.m_needs = needs # Quantity of items needed
        self.m_time = time # Critic time / Priority (more time -> minus priority)
        self.m_weather = weather # Weather
        

    def __str__(self):
        return "Node " + self.m_id + "\nName: " +self.m_name + "\nNeeds: " + self.m_needs 

    def __repr__(self):
        return "node " + self.m_name

    def setId(self, id):
        self.m_id = id

    def getId(self):
        return self.m_id

    def getName(self):
        return self.m_name
    
    def getNeeds(self):
        return self.m_needs
    
    def setNeeds(self, value):
        self.m_needs = value
    
    def getTime(self):
        return self.m_time

    def getWeather(self):   
        return self.m_weather
    
    def __eq__(self, other):
        return self.m_id == other.m_id  

    def __hash__(self):
        return hash(self.m_id)
