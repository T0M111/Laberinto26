"""
Patrón Bridge - Implementor.

Jerarquía Implementor del patrón Bridge:
  - Implementor     : Forma    (abstracta, define la interfaz geométrica)
  - ConcreteImpl A  : Cuadrado (4 lados cardinales: N, S, E, O)
  - ConcreteImpl B  : Rombo    (4 lados diagonales: NE, NO, SE, SO)

La Abstraction (Contenedor) referencia una Forma mediante +forma,
desacoplando la jerarquía de habitaciones de la jerarquía de formas geométricas.
"""
from abc import ABC, abstractmethod


class Forma(ABC):
    """
    Implementor del patrón Bridge.

    Define la interfaz que los ConcreteImplementors deben cumplir:
      +num          : número de lados de la forma
      +orientaciones: lista de objetos Orientacion que identifican cada lado
    """

    @property
    @abstractmethod
    def num(self) -> int:
        """Número de lados de la forma geométrica."""

    @property
    @abstractmethod
    def orientaciones(self) -> list:
        """Lista de instancias de Orientacion que corresponden a cada lado."""

    def __str__(self):
        nombres = ", ".join(str(o) for o in self.orientaciones)
        return f"{self.__class__.__name__}({self.num} lados: {nombres})"


class Cuadrado(Forma):
    """
    Concrete Implementor A.
    Forma cuadrada: 4 lados cardinales (Norte, Sur, Este, Oeste).
    """

    @property
    def num(self) -> int:
        return 4

    @property
    def orientaciones(self) -> list:
        from orientacion import Norte, Sur, Este, Oeste
        return [Norte(), Sur(), Este(), Oeste()]


class Rombo(Forma):
    """
    Concrete Implementor B.
    Forma rómbica: 4 lados diagonales (Noreste, Noroeste, Sureste, Suroeste).
    """

    @property
    def num(self) -> int:
        return 4

    @property
    def orientaciones(self) -> list:
        from orientacion import Noreste, Noroeste, Sureste, Suroeste
        return [Noreste(), Noroeste(), Sureste(), Suroeste()]
