"""
Clase LaberintoFuegoFactory - Factoría concreta del Abstract Factory.
Crea elementos del laberinto de fuego.
"""
from laberinto_factory import LaberintoFactory
from pared_fuego import ParedFuego
from puerta_fuego import PuertaFuego


class LaberintoFuegoFactory(LaberintoFactory):
    """
    Factoría concreta que produce paredes y puertas envueltas en fuego.
    """

    def fabricar_pared(self):
        """
        Crea una ParedFuego.

        Returns:
            Una nueva instancia de ParedFuego.
        """
        return ParedFuego()

    def fabricar_puerta(self):
        """
        Crea una PuertaFuego.

        Returns:
            Una nueva instancia de PuertaFuego.
        """
        return PuertaFuego()
