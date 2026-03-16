"""
Patrón Adapter - Adapter concreto.
BichoAdapter adapta la interfaz de Bicho (adaptee) a la interfaz Varita (target),
de modo que Personaje puede cambiar el modo de un Bicho sin conocerlo directamente.
"""
from varita import Varita
from bicho import Bicho


class BichoAdapter(Varita):
    """
    Adapter (GoF) que envuelve un Bicho y expone la interfaz Varita.

    - Target:  Varita.cambiarModo()
    - Adaptee: Bicho.cambiarModo()
    - Adapter: BichoAdapter — delega cambiarModo() al Bicho interno.
    """

    def __init__(self, bicho: Bicho):
        """
        Args:
            bicho: El Bicho cuyo modo será cambiado a través de este adaptador.
        """
        self.bicho = bicho

    def cambiarModo(self):
        """
        Implementación de la interfaz Varita.
        Delega la llamada al método cambiarModo() del Bicho adaptado.
        """
        self.bicho.cambiarModo()
