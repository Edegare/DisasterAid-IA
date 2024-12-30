class Node:
    def __init__(self, id, data=None):
        """
        Classe que representa um nó no grafo.

        :param id: Identificador único do nó.
        :param data: Dados adicionais associados ao nó.
        """
        self.id = id
        self.data = data

    def __repr__(self):
        return f"Node(id={self.id}, data={self.data})"
