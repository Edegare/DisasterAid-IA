# models/zone.py

class Zone:
    def __init__(self, id, priority, population, critical_time, vehicles=None):
        """
        Classe base para representar uma zona de entrega.

        :param id: Identificador único da zona.
        :param priority: Prioridade da zona (maior valor significa maior prioridade).
        :param population: Número de pessoas na zona.
        :param critical_time: Janela de tempo crítica para atendimento (em horas).
        :param vehicles: Lista de veículos associados à zona (opcional).
        """
        self.id = id
        self.priority = priority
        self.population = population
        self.critical_time = critical_time
        self.vehicles = vehicles

    def __repr__(self):
        return (f"Zone(id={self.id}, priority={self.priority}, population={self.population}, "
                f"critical_time={self.critical_time}, vehicles={self.vehicles})")


class NormalZone(Zone):
    def __init__(self, id, priority, population, critical_time):
        """
        Zona normal, sem veículos associados por padrão.
        """
        super().__init__(id, priority, population, critical_time, vehicles=None)


class SupplyZone(Zone):
    def __init__(self, id, priority, population, critical_time):
        """
        Zona de abastecimento, sem veículos associados por padrão.
        """
        super().__init__(id, priority, population, critical_time, vehicles=None)


class SupportZone(Zone):
    def __init__(self, id, priority, population, critical_time, vehicles):
        """
        Zona de suporte, com lista de veículos obrigatória.
        """
        super().__init__(id, priority, population, critical_time, vehicles=vehicles)
