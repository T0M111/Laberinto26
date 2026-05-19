"""
Clase Habitacion - Contenedor concreto del mapa (Composite).
Utiliza el patrón Strategy mediante objetos Orientacion.
"""
import random
from contenedor import Contenedor
from orientacion import Orientacion


class Habitacion(Contenedor):
    """
    Representa una habitación en el laberinto.
    Contenedor Composite: sus hijos son los elementos en sus lados
    (Pared, Puerta u otras Habitacion).
    Usa objetos Orientacion (Strategy) como claves para los lados.
    """

    def __init__(self, numero_habitacion=0):
        """
        Inicializa una habitación.

        Args:
            numero_habitacion: Identificador único de la habitación.
        """
        super().__init__()
        self.numero = numero_habitacion
        self.orientaciones = {}  # Dict[str, ElementoMapa]

    def establecer_lado(self, orientacion, elemento):
        """
        Establece un elemento (Pared, Puerta) en un lado de la habitación.
        El elemento se registra como hijo Composite y bajo su orientacion.

        Args:
            orientacion: Instancia de Orientacion (Norte, Sur, Este, Oeste).
            elemento: ElementoMapa a colocar en ese lado.
        """
        nombre = str(orientacion)
        # Si ya había un elemento en esa orientación, eliminarlo como hijo
        if nombre in self.orientaciones:
            self.eliminar_hijo(self.orientaciones[nombre])
        self.orientaciones[nombre] = elemento
        self.agregar_hijo(elemento)

    def obtener_lado(self, orientacion):
        """
        Obtiene el elemento en un lado específico.

        Args:
            orientacion: Instancia de Orientacion o string con el nombre.

        Returns:
            El elemento en ese lado o None si no existe.
        """
        return self.orientaciones.get(str(orientacion))

    def obtener_orientacion_aleatoria(self):
        """
        Devuelve un ElementoMapa aleatorio de entre los lados de la habitación.
        Usado por Modo.camina() para que el bicho intente moverse en una
        dirección aleatoria.
        """
        valores = list(self.orientaciones.values())
        return valores[random.randint(0, len(valores) - 1)]

    def __str__(self):
        """Representación en string de la habitación."""
        return f"Habitacion #{self.numero}"
