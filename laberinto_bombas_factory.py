"""
Clase LaberintoBombasFactory - Factoría concreta del Abstract Factory.
Crea elementos del laberinto con bombas.
"""
from laberinto_factory import LaberintoFactory
from pared_bomba import ParedBomba
from puerta_bomba import PuertaBomba


class LaberintoBombasFactory(LaberintoFactory):
    """
    Factoría concreta que produce paredes y puertas con bombas.
    """

    def fabricar_pared(self):
        """
        Crea una ParedBomba.

        Returns:
            Una nueva instancia de ParedBomba.
        """
        return ParedBomba()

    def fabricar_puerta(self):
        """
        Crea una PuertaBomba.

        Returns:
            Una nueva instancia de PuertaBomba.
        """
        return PuertaBomba()
