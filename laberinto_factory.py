"""
Clase LaberintoFactory - Abstract Factory.
Define la interfaz para crear los productos del laberinto.
"""
from abc import ABC, abstractmethod


class LaberintoFactory(ABC):
    """
    Factoría abstracta que declara los métodos para crear
    los distintos tipos de elementos del laberinto.
    Las subclases concretas determinan qué variante de cada
    producto se instancia.
    """

    @abstractmethod
    def fabricar_pared(self):
        """
        Crea y devuelve una instancia de Pared (o variante).

        Returns:
            Un objeto Pared o subclase de Pared.
        """

    @abstractmethod
    def fabricar_puerta(self):
        """
        Crea y devuelve una instancia de Puerta (o variante).

        Returns:
            Un objeto Puerta o subclase de Puerta.
        """
