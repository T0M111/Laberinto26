"""
Clase PuertaBomba - Producto concreto del Abstract Factory.
"""
from puerta import Puerta


class PuertaBomba(Puerta):
    """
    Variante de Puerta que contiene una bomba.
    Es el producto creado por LaberintoBombasFactory.
    """

    def __init__(self):
        super().__init__()
        self.con_bomba = True

    def __str__(self):
        estado = "abierta" if self.abierta else "cerrada"
        return f"PuertaBomba ({estado})"
