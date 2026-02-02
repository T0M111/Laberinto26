"""
Clase Pared - Elemento concreto del mapa.
"""
from elemento_mapa import ElementoMapa


class Pared(ElementoMapa):
    """
    Representa una pared en el laberinto.
    Es un elemento que bloquea el paso.
    """
    
    def __init__(self):
        """Inicializa una pared."""
        pass
    
    def __str__(self):
        """Representación en string de la pared."""
        return "Pared"
