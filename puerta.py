"""
Clase Puerta - Elemento concreto del mapa.
"""
from elemento_mapa import ElementoMapa


class Puerta(ElementoMapa):
    """
    Representa una puerta en el laberinto.
    Es un elemento que conecta dos habitaciones.
    """
    
    def __init__(self):
        """Inicializa una puerta."""
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
