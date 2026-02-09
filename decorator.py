"""
Patrón Decorator - Decorador base para elementos del mapa.
"""
from elemento_mapa import ElementoMapa


class Decorator(ElementoMapa):
    """
    Decorador abstracto que envuelve un ElementoMapa,
    permitiendo añadir comportamiento adicional.
    """

    def __init__(self, component):
        """
        Inicializa el decorador con un componente.

        Args:
            component: ElementoMapa que se decora.
        """
        self.component = component

    def __str__(self):
        """Delega la representación al componente decorado."""
        return self.component.__str__()
