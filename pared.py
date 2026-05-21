"""
Clase Pared - Hoja concreta del mapa (Composite).
"""
from hoja import Hoja


class Pared(Hoja):
    """
    Representa una pared en el laberinto.
    Es un elemento hoja que bloquea el paso; no contiene hijos.
    """

    def __init__(self):
        """Inicializa una pared."""
        super().__init__()
    
    def aceptar(self, visitador) -> None:
        """Patrón Visitor — doble despacho: llama a visitarPared."""
        visitador.visitarPared(self)

    def __str__(self):
        """Representación en string de la pared."""
        return "Pared"
