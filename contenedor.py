"""
Patrón Composite - Contenedor.
Clase abstracta para elementos del mapa que pueden contener otros
ElementoMapa como hijos (Laberinto, Habitacion).
"""
from elemento_mapa import ElementoMapa


class Contenedor(ElementoMapa):
    """
    Nodo compuesto del patrón Composite.
    Mantiene una referencia a su padre (+padre, cardinalidad 1)
    y una colección de hijos (+hijos, cardinalidad 1..*).
    """

    def __init__(self):
        super().__init__()
        self._hijos = []  # +hijos: List[ElementoMapa]

    # --- Gestión de hijos ---

    def agregar_hijo(self, hijo: ElementoMapa):
        """
        Agrega un ElementoMapa como hijo de este contenedor.

        Args:
            hijo: Elemento a agregar.
        """
        hijo.padre = self
        self._hijos.append(hijo)

    def eliminar_hijo(self, hijo: ElementoMapa):
        """
        Elimina un ElementoMapa de la lista de hijos.

        Args:
            hijo: Elemento a eliminar.
        """
        if hijo in self._hijos:
            hijo.padre = None
            self._hijos.remove(hijo)

    def obtener_hijos(self):
        """
        Devuelve la lista de hijos de este contenedor.

        Returns:
            Lista de ElementoMapa hijos.
        """
        return list(self._hijos)

    def recorrer(self):
        """
        Iterador interno para un Contenedor (Iterator, recorrido en profundidad pre-order).
        Genera este nodo primero y luego recorre recursivamente cada hijo.
        Los hijos pueden ser Hojas o Contenedores; se delega en su propio recorrer().
        """
        yield self
        for hijo in self._hijos:
            yield from hijo.recorrer()
