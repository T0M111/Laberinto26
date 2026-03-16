"""
Clase ParedFuego - Producto concreto del Abstract Factory.
"""
from pared import Pared


class ParedFuego(Pared):
    """
    Variante de Pared que está envuelta en llamas.
    Es el producto creado por LaberintoFuegoFactory.
    """

    def __init__(self):
        super().__init__()
        self.en_llamas = True

    def __str__(self):
        return "ParedFuego"
