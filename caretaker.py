"""
Patrón Memento — clase Caretaker.

El Caretaker custodia el Memento sin inspeccionar ni modificar su contenido.
Proporciona operaciones convenientes de guardar y restaurar
que delegan en el Originator (Laberinto).

Roles:
  - Caretaker: este fichero — +memento (1).
"""
from memento import Memento


class Caretaker:
    """
    Patrón Memento — custodia el Memento.

    Mantiene una referencia al Memento (+memento, cardinalidad 1)
    sin acceder a su contenido interno.

    Atributos:
        memento (Memento | None): el Memento custodiado.
    """

    def __init__(self):
        self.memento = None  # +memento : Memento  [1]

    def guardar(self, laberinto) -> None:
        """
        Pide al Originator que cree un Memento y lo custodia.

        Args:
            laberinto: Laberinto (Originator) cuyo estado se guarda.
        """
        self.memento = laberinto.crearMemento()

    def restaurar(self, laberinto) -> None:
        """
        Pide al Originator que restaure su estado desde el Memento custodiado.

        Args:
            laberinto: Laberinto (Originator) a restaurar.

        Raises:
            ValueError: si no hay ningún Memento guardado.
        """
        if self.memento is None:
            raise ValueError("No hay ninguna partida guardada para restaurar.")
        laberinto.cargarPartida(self.memento)
