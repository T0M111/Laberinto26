"""
Clase Builder - Interfaz abstracta del patrón Builder.
Define el método fabricarLaberinto() que las subclases concretas deben implementar.
"""
from abc import ABC, abstractmethod


class Builder(ABC):
    """
    Interfaz abstracta del Builder.
    Declara el paso de construcción que el Director invocará.
    """

    @abstractmethod
    def fabricarLaberinto(self):
        """
        Construye y devuelve un Laberinto completo.

        Returns:
            Una instancia de Laberinto (o subclase) completamente configurada.
        """
