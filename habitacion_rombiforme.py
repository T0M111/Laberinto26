"""
Patrón Bridge - Abstraction refinada: HabitacionRombiforme.

Roles:
  - Abstraction         : Contenedor  (+forma: Forma)
  - Refined Abstraction : HabitacionRombiforme  (este fichero)
  - Implementor         : Forma
  - Concrete Implementor: Rombo

HabitacionRombiforme es una Habitacion cuya forma geométrica es un Rombo.
Sus lados se acceden mediante las cuatro orientaciones diagonales (NE, NO, SE, SO).
"""
from habitacion import Habitacion
from forma import Rombo
from pared import Pared


class HabitacionRombiforme(Habitacion):
    """
    Refined Abstraction del patrón Bridge.
    Habitación de planta rómbica: delega la descripción geométrica en Rombo.
    Por defecto inicializa los cuatro lados diagonales con Pared.
    """

    def __init__(self, numero: int = 0):
        """
        Args:
            numero: Identificador de la habitación.
        """
        super().__init__(numero)
        self.forma = Rombo()  # Bridge: enlace con el Implementor
        # Inicializar todos los lados diagonales con paredes por defecto
        for orientacion in self.forma.orientaciones:
            self.establecer_lado(orientacion, Pared())

    def __str__(self):
        return f"HabitacionRombiforme #{self.numero}"
