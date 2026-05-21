"""
Patrón Bridge - Abstraction refinada: HabitacionCuadrada.

Roles:
  - Abstraction         : Contenedor  (+forma: Forma)
  - Refined Abstraction : HabitacionCuadrada  (este fichero)
  - Implementor         : Forma
  - Concrete Implementor: Cuadrado

HabitacionCuadrada es una Habitacion cuya forma geométrica es un Cuadrado.
Sus lados se acceden mediante las cuatro orientaciones cardinales (N, S, E, O).
"""
from habitacion import Habitacion
from forma import Cuadrado
from pared import Pared


class HabitacionCuadrada(Habitacion):
    """
    Refined Abstraction del patrón Bridge.
    Habitación de planta cuadrada: delega la descripción geométrica en Cuadrado.
    Por defecto inicializa los cuatro lados cardinales con Pared.
    """

    def __init__(self, numero: int = 0):
        """
        Args:
            numero: Identificador de la habitación.
        """
        super().__init__(numero)
        self.forma = Cuadrado()  # Bridge: enlace con el Implementor
        # Inicializar todos los lados cardinales con paredes por defecto
        for orientacion in self.forma.orientaciones:
            self.establecer_lado(orientacion, Pared())

    def __str__(self):
        return f"HabitacionCuadrada #{self.numero}"
