"""
Patrón Command — ConcreteCommand Cerrar.
"""
from comando import Comando


class Cerrar(Comando):
    """
    Patrón Command — ConcreteCommand que cierra el receptor (Puerta).
    ejecutar() delega en receptor.cerrar().
    """

    def ejecutar(self) -> None:
        """Cierra la puerta receptora."""
        self.receptor.cerrar()
