"""
Patrón Flyweight — clase abstracta Moneda.

Estado intrínseco (compartido, inmutable por tipo): value
  → definido en cada ConcreteFlyweight (Oro, Plata, SuperMoneda).

Estado extrínseco (por uso): posicion
  → establecido desde fuera antes de cada uso (habitacion que contiene la moneda).
"""
from abc import ABC, abstractmethod


class Moneda(ABC):
    """
    Patrón Flyweight — interfaz Flyweight.

    Atributos:
        posicion: estado extrínseco — habitación donde se encuentra la moneda.

    Propiedad abstracta:
        value: estado intrínseco — valor en puntos del tipo de moneda.
    """

    def __init__(self):
        self.posicion = None  # extrinsic state (establecido por el cliente)

    @property
    @abstractmethod
    def value(self) -> int:
        """Valor intrínseco de la moneda (inmutable por tipo)."""
        pass

    def __str__(self):
        pos = f" en {self.posicion}" if self.posicion is not None else ""
        return f"{self.__class__.__name__}(value={self.value}{pos})"
