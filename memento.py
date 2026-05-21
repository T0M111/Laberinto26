"""
Patrón Memento — clase Memento.

Almacena una instantánea (snapshot) del estado interno de un Originator
(Laberinto) sin exponer su implementación.

Roles:
  - Memento: este fichero — guarda y devuelve el estado con getEstado/setEstado.
"""


class Memento:
    """
    Patrón Memento — almacena el estado del Originator.

    El Originator (Laberinto) crea Mementos con crearMemento() y
    los restaura con cargarPartida(). El Caretaker los custodia.

    Atributos:
        _estado: snapshot del estado interno del Laberinto
                 (copia profunda de su colección de habitaciones).
    """

    def __init__(self, estado):
        """
        Inicializa el Memento con el estado proporcionado.

        Args:
            estado: snapshot del estado interno del Originator.
        """
        self._estado = estado

    def getEstado(self):
        """Devuelve el estado guardado en este Memento."""
        return self._estado

    def setEstado(self, estado):
        """
        Reemplaza el estado guardado en este Memento.

        Args:
            estado: nuevo estado a guardar.
        """
        self._estado = estado
