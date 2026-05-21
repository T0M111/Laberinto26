"""
Patrón Visitor — ConcreteVisitor: VisitadorContador.

Recorre la jerarquía de ElementoMapa y cuenta cuántos elementos
de cada tipo hay en el laberinto.
"""
from visitador import Visitador


class VisitadorContador(Visitador):
    """
    Patrón Visitor — ConcreteVisitor que cuenta elementos por tipo.

    Atributos:
        habitaciones (int): número de Habitacion visitadas.
        puertas      (int): número de Puerta visitadas.
        paredes      (int): número de Pared visitadas.
    """

    def __init__(self):
        self.habitaciones = 0
        self.puertas = 0
        self.paredes = 0

    def visitarHabitacion(self, habitacion) -> None:
        """Incrementa el contador de habitaciones."""
        self.habitaciones += 1

    def visitarPuerta(self, puerta) -> None:
        """Incrementa el contador de puertas."""
        self.puertas += 1

    def visitarPared(self, pared) -> None:
        """Incrementa el contador de paredes."""
        self.paredes += 1

    def __str__(self):
        return (
            f"VisitadorContador("
            f"habitaciones={self.habitaciones}, "
            f"puertas={self.puertas}, "
            f"paredes={self.paredes})"
        )
