"""
Patrón Strategy - Orientación.
Clase abstracta Orientacion y sus estrategias concretas: Norte, Sur, Este, Oeste.
"""
from abc import ABC, abstractmethod


class Orientacion(ABC):
    """
    Clase abstracta que define la interfaz Strategy para las orientaciones
    de los lados de una Habitacion.
    """

    @abstractmethod
    def obtener_nombre(self):
        """Devuelve el nombre de la orientación."""
        pass

    def __str__(self):
        return self.obtener_nombre()


class Norte(Orientacion):
    """Estrategia concreta: orientación Norte."""

    def obtener_nombre(self):
        return "Norte"


class Sur(Orientacion):
    """Estrategia concreta: orientación Sur."""

    def obtener_nombre(self):
        return "Sur"


class Este(Orientacion):
    """Estrategia concreta: orientación Este."""

    def obtener_nombre(self):
        return "Este"


class Oeste(Orientacion):
    """Estrategia concreta: orientación Oeste."""

    def obtener_nombre(self):
        return "Oeste"
