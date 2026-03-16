"""
Patrón Adapter - Cliente.
Personaje interactúa únicamente con la interfaz Varita para cambiar
el modo de un bicho, sin necesidad de conocer la clase Bicho.
"""
from varita import Varita


class Personaje:
    """
    Cliente del patrón Adapter.
    Pide a su Varita que cambie el modo del objeto subyacente.
    No sabe (ni necesita saber) si la Varita envuelve un Bicho u otra entidad.
    """

    def __init__(self, nombre: str, varita: Varita):
        """
        Args:
            nombre:  Nombre identificador del personaje.
            varita:  Varita (o BichoAdapter) que el personaje usará.
        """
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
