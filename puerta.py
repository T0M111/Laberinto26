"""
Clase Puerta - Hoja concreta del mapa (Composite).
"""
from hoja import Hoja


class Puerta(Hoja):
    """
    Representa una puerta en el laberinto.
    Es un elemento hoja que conecta dos habitaciones; no contiene hijos.
    """

    def __init__(self):
        """Inicializa una puerta."""
        super().__init__()
        self.abierta = False
    
    def abrir(self):
        """Abre la puerta."""
        self.abierta = True
    
    def cerrar(self):
        """Cierra la puerta."""
        self.abierta = False
    
    def __str__(self):
        """Representación en string de la puerta."""
        estado = "abierta" if self.abierta else "cerrada"
        return f"Puerta ({estado})"
