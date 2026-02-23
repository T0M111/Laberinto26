"""
Patrón Strategy - Modo de comportamiento de un Bicho.
Clase abstracta Modo y sus estrategias concretas: Agresivo, Perezoso.
"""
from abc import ABC, abstractmethod


class Modo(ABC):
    """
    Clase abstracta que define la interfaz Strategy para el comportamiento
    de un Bicho dentro del laberinto.
    """

    @abstractmethod
    def ejecutar(self, bicho):
        """
        Ejecuta el comportamiento correspondiente al modo.

        Args:
            bicho: El Bicho que actúa según este modo.
        """
        pass

    @abstractmethod
    def obtener_nombre(self):
        """Devuelve el nombre del modo."""
        pass

    def __str__(self):
        return self.obtener_nombre()


class Agresivo(Modo):
    """Estrategia concreta: el bicho ataca activamente."""

    def obtener_nombre(self):
        return "Agresivo"

    def ejecutar(self, bicho):
        print(f"{bicho} actúa en modo Agresivo: ¡Busca y ataca!")


class Perezoso(Modo):
    """Estrategia concreta: el bicho descansa sin hacer nada."""

    def obtener_nombre(self):
        return "Perezoso"

    def ejecutar(self, bicho):
        print(f"{bicho} actúa en modo Perezoso: descansa tranquilamente.")
