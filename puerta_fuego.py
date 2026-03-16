"""
Clase PuertaFuego - Producto concreto del Abstract Factory.
"""
from puerta import Puerta


class PuertaFuego(Puerta):
    """
    Variante de Puerta envuelta en llamas.
    Es el producto creado por LaberintoFuegoFactory.
    """

    def __init__(self):
        super().__init__()
        self.en_llamas = True

    def __str__(self):
        estado = "abierta" if self.abierta else "cerrada"
        return f"PuertaFuego ({estado})"
