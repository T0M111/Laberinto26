"""
Clase Director - Director del patrón Builder.
Orquesta la construcción delegando en un objeto Builder.
"""


class Director:
    """
    Director que conoce los pasos de construcción y los delega en el Builder.
    No sabe qué productos concretos se están creando: solo invoca
    fabricarLaberinto() sobre el builder que se le haya inyectado.
    """

    def __init__(self, builder):
        """
        Inicializa el Director con un Builder concreto.

        Args:
            builder: Instancia de Builder (o subclase) que realizará la construcción.
        """
        self.builder = builder

    def procesar(self):
        """
        Dirige la construcción completa del laberinto.

        Returns:
            El Laberinto construido por el Builder.
        """
        return self.builder.fabricarLaberinto()
