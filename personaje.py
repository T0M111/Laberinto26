"""
Clase Personaje - Colleague concreto B del patrón Mediator.
Hereda de Ente y actúa como cliente del patrón Adapter (Varita).
"""
from varita import Varita
from ente import Ente


class Personaje(Ente):
    """
    Colleague B del patrón Mediator.
    Hereda de Ente: vidas, poder, estado y referencia al Mediador (_juego).
    Mantiene además su rol de cliente del Adapter: usa una Varita (opcional)
    para cambiar el modo de un Bicho sin acoplarse a él directamente.
    """

    def __init__(self, nombre: str, varita: Varita = None,
                 vidas: int = 5, poder: int = 2):
        """
        Args:
            nombre: Nombre identificador del personaje.
            varita: Varita (o BichoAdapter) que el personaje usará (opcional).
            vidas:  Puntos de vida (por defecto 5).
            poder:  Daño que inflige por ataque (por defecto 2).
        """
        super().__init__(vidas=vidas, poder=poder)
        self.nombre = nombre
        self.varita = varita

    def pedir_cambio_modo(self):
        """
        El personaje pide cambiar el modo a través de su Varita.
        Delega completamente en varita.cambiarModo().
        """
        print(f"  {self.nombre} agita su varita...")
        self.varita.cambiarModo()

    def __str__(self):
        return f"Personaje({self.nombre})"
