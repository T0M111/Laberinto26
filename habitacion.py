"""
Clase Habitacion - Elemento concreto del mapa.
Utiliza el patrón Strategy mediante objetos Orientacion.
"""
from elemento_mapa import ElementoMapa
from orientacion import Orientacion


class Habitacion(ElementoMapa):
    """
    Representa una habitación en el laberinto.
    Puede contener puertas y paredes en sus lados.
    Utiliza objetos Orientacion (Strategy) como claves para los lados.
    """

    def __init__(self, numero_habitacion=0):
        """
        Inicializa una habitación.

        Args:
            numero_habitacion: Identificador único de la habitación.
        """
        self.numero = numero_habitacion
        self.orientaciones = {}  # Dict[Orientacion, ElementoMapa]

    def establecer_lado(self, orientacion, elemento):
        """
        Establece un elemento (Pared, Puerta) en un lado de la habitación.

        Args:
            orientacion: Instancia de Orientacion (Norte, Sur, Este, Oeste).
            elemento: ElementoMapa a colocar en ese lado.
        """
        self.orientaciones[str(orientacion)] = elemento

    def obtener_lado(self, orientacion):
        """
        Obtiene el elemento en un lado específico.

        Args:
            orientacion: Instancia de Orientacion o string con el nombre.

        Returns:
            El elemento en ese lado o None si no existe.
        """
        return self.orientaciones.get(str(orientacion))

    def __str__(self):
        """Representación en string de la habitación."""
        return f"Habitacion #{self.numero}"
