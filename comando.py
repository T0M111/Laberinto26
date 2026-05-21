"""
Patrón Command — Clase abstracta Comando.

Roles:
  - Command (abstracto): define la interfaz ejecutar() y mantiene el receptor.
"""
from abc import ABC, abstractmethod


class Comando(ABC):
    """
    Patrón Command — interfaz abstracta.

    Atributos:
        receptor: objeto sobre el que se ejecuta la acción (p.ej. Puerta).

    Métodos:
        ejecutar(): operación concreta definida por cada subclase.
    """

    def __init__(self, receptor):
        self.receptor = receptor

    @abstractmethod
    def ejecutar(self) -> None:
        """Ejecuta la acción encapsulada sobre el receptor."""
        pass
