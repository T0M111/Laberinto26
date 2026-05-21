"""
Patrón Observer — interfaz abstracta del Observer.

Roles:
  - Subject          : Juego           (juego.py)
  - Observer         : Observador      (este fichero — abstracto)
  - ConcreteObserver : LaberintoGUI    (laberinto_gui.py)

Cualquier clase que quiera recibir notificaciones de Juego debe
heredar de Observador e implementar actualizar(juego).
"""
from abc import ABC, abstractmethod


class Observador(ABC):
    """
    Observer abstracto del patrón Observer.
    Las subclases concretas implementan actualizar() para reaccionar
    a los cambios de estado del Subject (Juego).
    """

    @abstractmethod
    def actualizar(self, juego) -> None:
        """
        Notificación de cambio de estado en el Subject.

        Args:
            juego: El Subject (Juego) que emite la notificación.
                   El Observer puede consultar su estado directamente
                   (variante pull del patrón Observer).
        """
