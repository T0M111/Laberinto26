"""
Clase Bomba - Decorador concreto de ElementoMapa.
"""
from decorator import Decorator


class Bomba(Decorator):
    """
    Decorador que añade comportamiento de bomba
    a un elemento del mapa.
    """

    def __init__(self, component):
        """
        Inicializa la bomba decorando un componente.

        Args:
            component: ElementoMapa que se decora con bomba.
        """
        super().__init__(component)
        self.activa = True

    def explotar(self):
        """Hace explotar la bomba."""
        self.activa = False

    def __str__(self):
        estado = "activa" if self.activa else "explotada"
        return f"Bomba ({estado}) sobre {self.component}"
