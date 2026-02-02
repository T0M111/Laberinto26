"""
Clase abstracta base para todos los elementos del mapa del laberinto.
Patrón de diseño: Factory Method
"""
from abc import ABC, abstractmethod


class ElementoMapa(ABC):
    """
    Clase abstracta que representa un elemento genérico del mapa.
    Todos los elementos del laberinto (Pared, Puerta, Habitacion, Laberinto)
    heredan de esta clase.
    """
    
    @abstractmethod
    def __str__(self):
        """Representación en string del elemento."""
        pass
