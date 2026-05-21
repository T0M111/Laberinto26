"""
Patrón Prototype — ConcretePrototype A.

Roles:
  - Prototype          : Laberinto        (laberinto.py)
  - ConcretePrototype A: LaberintoCuadrado (este fichero)

LaberintoCuadrado es un laberinto cuyos elementos son HabitacionCuadrada
(Bridge: Cuadrado como Forma). clone() devuelve una copia profunda tipada.
"""
import copy
from laberinto import Laberinto


class LaberintoCuadrado(Laberinto):
    """
    ConcretePrototype A del patrón Prototype.
    Laberinto compuesto por HabitacionCuadrada (Bridge).
    Sobrescribe clone() para garantizar que la copia es también un
    LaberintoCuadrado.
    """

    def clone(self):
        """
        Prototype: devuelve una copia profunda de este LaberintoCuadrado.

        Returns:
            Nueva instancia de LaberintoCuadrado con todos los elementos copiados.
        """
        return copy.deepcopy(self)

    def __str__(self):
        return f"LaberintoCuadrado con {len(self.habitaciones)} habitaciones"
