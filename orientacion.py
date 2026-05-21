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
    """
    Estrategia concreta: orientación Norte.
    Implementa el patrón Singleton: solo existe una instancia de Norte.
    """

    unicaInstancia = None

    def __new__(cls):
        if cls.unicaInstancia is None:
            cls.unicaInstancia = super().__new__(cls)
        return cls.unicaInstancia

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


# --- Orientaciones diagonales (usadas por Rombo en el patrón Bridge) ---

class Noreste(Orientacion):
    """Estrategia concreta: orientación Noreste (diagonal NE)."""

    def obtener_nombre(self):
        return "Noreste"


class Noroeste(Orientacion):
    """Estrategia concreta: orientación Noroeste (diagonal NO)."""

    def obtener_nombre(self):
        return "Noroeste"


class Sureste(Orientacion):
    """Estrategia concreta: orientación Sureste (diagonal SE)."""

    def obtener_nombre(self):
        return "Sureste"


class Suroeste(Orientacion):
    """Estrategia concreta: orientación Suroeste (diagonal SO)."""

    def obtener_nombre(self):
        return "Suroeste"
