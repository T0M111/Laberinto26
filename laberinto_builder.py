"""
Clase LaberintoBuilder - Builder concreto del patrón Builder.
Implementa fabricarLaberinto() construyendo un Laberinto completo.
"""
from builder import Builder
from laberinto import Laberinto
from habitacion import Habitacion
from pared import Pared
from puerta import Puerta
from orientacion import Norte, Sur, Este, Oeste


class LaberintoBuilder(Builder):
    """
    Builder concreto que ensambla un Laberinto estándar con dos habitaciones
    conectadas por una puerta.
    """

    def fabricarLaberinto(self):
        """
        Construye un Laberinto con dos habitaciones y una puerta compartida.

        Returns:
            Un Laberinto completamente configurado.
        """
        laberinto = Laberinto()

        h1 = Habitacion(1)
        h2 = Habitacion(2)
        puerta = Puerta()

        h1.establecer_lado(Norte(), Pared())
        h1.establecer_lado(Este(), puerta)
        h1.establecer_lado(Sur(), Pared())
        h1.establecer_lado(Oeste(), Pared())

        h2.establecer_lado(Norte(), Pared())
        h2.establecer_lado(Este(), Pared())
        h2.establecer_lado(Sur(), Pared())
        h2.establecer_lado(Oeste(), puerta)

        laberinto.agregar_habitacion(h1)
        laberinto.agregar_habitacion(h2)

        return laberinto
