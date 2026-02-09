"""
Clase Hechizo - Decorador concreto de ElementoMapa.
"""
from decorator import Decorator


class Hechizo(Decorator):
    """
    Decorador que añade un hechizo
    a un elemento del mapa.
    """

    def __init__(self, component):
        """
        Inicializa el hechizo decorando un componente.

        Args:
            component: ElementoMapa que se decora con hechizo.
        """
        super().__init__(component)
        self.activo = True

    def aplicar(self):
        """Aplica el hechizo."""
        self.activo = False

    def __str__(self):
        estado = "activo" if self.activo else "usado"
        return f"Hechizo ({estado}) sobre {self.component}"
