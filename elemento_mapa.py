"""
Clase abstracta base para todos los elementos del mapa del laberinto.
Patrón de diseño: Factory Method + Composite
"""
from abc import ABC, abstractmethod


class ElementoMapa(ABC):
    """
    Componente del patrón Composite.
    Clase abstracta que representa un elemento genérico del mapa.
    Todos los elementos del laberinto (Pared, Puerta, Habitacion, Laberinto)
    heredan de esta clase.
    Define la interfaz común para hojas y contenedores.
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
    def __str__(self):
        """Representación en string del elemento."""
        pass
