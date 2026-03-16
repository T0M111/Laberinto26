"""
Patrón Adapter - Interfaz objetivo (Target).
Varita define la interfaz que Personaje utiliza para cambiar el modo de un bicho.
"""
from abc import ABC, abstractmethod


class Varita(ABC):
    """
    Interfaz objetivo del patrón Adapter.
    Personaje solo conoce esta interfaz; no sabe si está
    hablando con una varita real o con un BichoAdapter.
    """

    @abstractmethod
    def cambiarModo(self):
        """Cambia el modo del objeto subyacente."""
        pass
