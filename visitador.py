"""
Patrón Visitor — clase abstracta Visitador.

Define la interfaz de visita para todos los ElementoMapa concretos
que implementan +aceptar(Visitor). El doble despacho se completa
cuando cada elemento llama al método visit correspondiente.

Métodos:
  visitarHabitacion(h)  — llamado por Habitacion.aceptar()
  visitarPuerta(p)      — llamado por Puerta.aceptar()
  visitarPared(p)       — llamado por Pared.aceptar()
"""
from abc import ABC, abstractmethod


class Visitador(ABC):
    """
    Patrón Visitor — interfaz abstracta del Visitante.

    Cada subclase concreta implementa una operación diferente
    sobre la jerarquía de ElementoMapa sin alterar esas clases.
    """

    @abstractmethod
    def visitarHabitacion(self, habitacion) -> None:
        """Visita una Habitacion (o subclase: HabitacionCuadrada, etc.)."""
        pass

    @abstractmethod
    def visitarPuerta(self, puerta) -> None:
        """Visita una Puerta (o subclase: PuertaBomba, PuertaFuego, etc.)."""
        pass

    @abstractmethod
    def visitarPared(self, pared) -> None:
        """Visita una Pared (o subclase: ParedBomba, ParedFuego, etc.)."""
        pass
