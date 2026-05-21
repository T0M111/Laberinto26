"""
Patrón Command — ConcreteCommand Abrir.
"""
from comando import Comando


class Abrir(Comando):
    """
    Patrón Command — ConcreteCommand que abre el receptor (Puerta).
    ejecutar() delega en receptor.abrir().
    """

    def ejecutar(self) -> None:
        """Abre la puerta receptora."""
        self.receptor.abrir()
