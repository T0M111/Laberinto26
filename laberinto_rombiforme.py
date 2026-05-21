"""
Patrón Prototype — ConcretePrototype B.

Roles:
  - Prototype          : Laberinto            (laberinto.py)
  - ConcretePrototype B: LaberintoRombiforme  (este fichero)

LaberintoRombiforme es un laberinto cuyos elementos son HabitacionRombiforme
(Bridge: Rombo como Forma). clone() devuelve una copia profunda tipada.
"""
import copy
from laberinto import Laberinto


class LaberintoRombiforme(Laberinto):
    """
    ConcretePrototype B del patrón Prototype.
    Laberinto compuesto por HabitacionRombiforme (Bridge).
    Sobrescribe clone() para garantizar que la copia es también un
    LaberintoRombiforme.
    """

    def clone(self):
        """
        Prototype: devuelve una copia profunda de este LaberintoRombiforme.

        Returns:
            Nueva instancia de LaberintoRombiforme con todos los elementos copiados.
        """
        return copy.deepcopy(self)

    def __str__(self):
        return f"LaberintoRombiforme con {len(self.habitaciones)} habitaciones"
