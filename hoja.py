"""
Patrón Composite - Hoja.
Clase abstracta para elementos del mapa sin hijos (Pared, Puerta).
"""
from elemento_mapa import ElementoMapa


class Hoja(ElementoMapa):
    """
    Nodo hoja del patrón Composite.
    Los elementos hoja no contienen otros ElementoMapa.
    Sobreescribe los métodos de gestión de hijos para que
    informen claramente que no están soportados.
    """

    def __init__(self):
        super().__init__()

    def agregar_hijo(self, hijo):
        raise TypeError(f"{self.__class__.__name__} es una hoja y no acepta hijos")

    def eliminar_hijo(self, hijo):
        raise TypeError(f"{self.__class__.__name__} es una hoja y no acepta hijos")

    def obtener_hijos(self):
        return []

    def recorrer(self):
        """
        Iterador interno para una Hoja.
        Una hoja no tiene hijos, por lo que sólo se genera a sí misma.
        """
        yield self
