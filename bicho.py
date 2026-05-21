"""
Clase Bicho - Colleague concreto A del patrón Mediator.
Hereda de Ente y utiliza el patrón Strategy mediante objetos Modo.
"""
from modo import Modo
from ente import Ente


class Bicho(Ente):
    """
    Colleague A del patrón Mediator.
    Representa un bicho (enemigo) dentro del laberinto.
    Su comportamiento está delegado en un objeto Modo (Strategy),
    que puede cambiar en tiempo de ejecución.
    Hereda de Ente: vidas, poder, estado y referencia al Mediador (_juego).
    """

    def __init__(self, nombre, modo: Modo, vidas: int = 3, poder: int = 1):
        """
        Inicializa un Bicho con un nombre, modo de comportamiento y estadísticas.

        Args:
            nombre: Nombre identificador del bicho.
            modo:   Instancia de Modo que define su comportamiento actual.
            vidas:  Puntos de vida (por defecto 3).
            poder:  Daño que inflige por ataque (por defecto 1).
        """
        super().__init__(vidas=vidas, poder=poder)
        self.nombre = nombre
        self.modo = modo
        self.posicion = None  # Habitacion donde se encuentra actualmente

    def establecer_modo(self, modo: Modo):
        """
        Cambia el modo de comportamiento del bicho en tiempo de ejecución.

        Args:
            modo: Nueva instancia de Modo.
        """
        self.modo = modo

    def actuar(self):
        """
        Patrón State: comprueba primero si el ente puede actuar
        (super().actuar() → estado.puedeActuar()). Si puede, delega
        el comportamiento en el modo actual (Strategy).

        Returns:
            True si el bicho pudo actuar, False si estaba muerto.
        """
        puede = super().actuar()
        if puede:
            self.modo.actua(self)
        return puede

    def cambiarModo(self):
        """
        Adaptee del patrón Adapter.
        Delega el cambio de modo en el propio objeto Modo actual
        (doble despacho): cada subclase de Modo sabe a qué modo transicionar.
        """
        self.modo.cambiarModo(self)

    def __str__(self):
        return f"Bicho({self.nombre}, modo={self.modo})"
