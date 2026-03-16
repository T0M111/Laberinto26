"""
Clase ParedBomba - Producto concreto del Abstract Factory.
"""
from pared import Pared


class ParedBomba(Pared):
    """
    Variante de Pared que contiene una bomba.
    Es el producto creado por LaberintoBombasFactory.
    """

    def __init__(self):
        super().__init__()
        self.con_bomba = True

    def __str__(self):
        return "ParedBomba"
