"""
Patrón State aplicado al ciclo de vida de un Ente.

Roles:
  - Context        : Ente  (ver ente.py)
  - State          : Estado          — clase abstracta, define puedeActuar()
  - ConcreteStateA : Vivo            — el ente puede actuar (puedeActuar → True)
  - ConcreteStateB : Muerto          — el ente no puede actuar (puedeActuar → False)

Ente.actuar() delega en self.estado.puedeActuar() para decidir si la
acción procede; el comportamiento concreto lo implementa cada subclase.
"""
from abc import ABC, abstractmethod


class Estado(ABC):
    """
    State abstracto del patrón State.
    Define la interfaz que el Contexto (Ente) usa para consultar
    si puede llevar a cabo una acción.
    """

    @abstractmethod
    def puedeActuar(self) -> bool:
        """Devuelve True si el ente asociado puede actuar en este estado."""

    @abstractmethod
    def __str__(self) -> str:
        pass


class Vivo(Estado):
    """ConcreteState A: el ente está vivo y puede actuar."""

    def puedeActuar(self) -> bool:
        return True

    def __str__(self):
        return "Vivo"


class Muerto(Estado):
    """ConcreteState B: el ente ha sido eliminado y no puede actuar."""

    def puedeActuar(self) -> bool:
        return False

    def __str__(self):
        return "Muerto"
