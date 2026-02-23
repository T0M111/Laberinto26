"""
Clase Bicho - Entidad del laberinto con comportamiento variable.
Utiliza el patrón Strategy mediante objetos Modo.
"""
from modo import Modo


class Bicho:
    """
    Representa un bicho (enemigo) dentro del laberinto.
    Su comportamiento está delegado en un objeto Modo (Strategy),
    que puede cambiar en tiempo de ejecución.
    """

    def __init__(self, nombre, modo: Modo):
        """
        Inicializa un Bicho con un nombre y un modo de comportamiento.

        Args:
            nombre: Nombre identificador del bicho.
            modo: Instancia de Modo que define su comportamiento actual.
        """
        self.nombre = nombre
        self.modo = modo

    def establecer_modo(self, modo: Modo):
        """
        Cambia el modo de comportamiento del bicho en tiempo de ejecución.

        Args:
            modo: Nueva instancia de Modo.
        """
        self.modo = modo

    def actuar(self):
        """
        Delega la acción al modo actual (Strategy).
        El método actua() del Modo es un Template Method que llama
        a ataca() y duerme() según la subclase concreta.
        """
        self.modo.actua(self)

    def __str__(self):
        return f"Bicho({self.nombre}, modo={self.modo})"
