"""
Clase abstracta base para todos los elementos del mapa del laberinto.
Patrones de diseño: Factory Method + Composite + Iterator
"""
from abc import ABC, abstractmethod


class ElementoMapa(ABC):
    """
    Componente del patrón Composite.
    Clase abstracta que representa un elemento genérico del mapa.
    Todos los elementos del laberinto (Pared, Puerta, Habitacion, Laberinto)
    heredan de esta clase.
    Define la interfaz común para hojas y contenedores.

    Implementa el patrón Iterator mediante el método +recorrer():
    - Las hojas se generan a sí mismas.
    - Los contenedores se generan a sí mismos y luego recorren sus hijos.
    - __iter__ delega en recorrer() para soportar el iterador externo de Python.
    """

    def __init__(self):
        self.padre = None  # Referencia al Contenedor padre (Composite)

    def agregar_hijo(self, hijo):
        """Disponible sólo en Contenedor. Las Hojas lanzan error."""
        raise NotImplementedError(f"{self.__class__.__name__} no admite hijos")

    def eliminar_hijo(self, hijo):
        """Disponible sólo en Contenedor. Las Hojas lanzan error."""
        raise NotImplementedError(f"{self.__class__.__name__} no admite hijos")

    def obtener_hijos(self):
        """Disponible sólo en Contenedor. Las Hojas lanzan error."""
        raise NotImplementedError(f"{self.__class__.__name__} no tiene hijos")

    @abstractmethod
    def recorrer(self):
        """
        Iterador interno (Iterator).
        Genera en profundidad todos los ElementoMapa del subárbol,
        empezando por el propio nodo (pre-order).
        Las subclases concretas implementan la estrategia adecuada.
        """
        pass

    def __iter__(self):
        """
        Iterador externo: permite usar `for elem in elemento_mapa`.
        Delega en recorrer() para recorrer el subárbol Composite.
        """
        return self.recorrer()

    @abstractmethod
    def __str__(self):
        """Representación en string del elemento."""
        pass
