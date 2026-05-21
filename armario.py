"""
Patrón Visitor — Armario (nuevo Contenedor concreto).

Armario es un Contenedor que puede guardar elementos del mapa
(p.ej. objetos, armas, hechizos). Su aceptar() propaga la visita
a todos sus hijos sin llamar a un método visitarArmario propio
(el visitador recorre su contenido, no el armario en sí).
"""
from contenedor import Contenedor


class Armario(Contenedor):
    """
    Patrón Composite — Contenedor concreto para almacenar objetos.
    Patrón Visitor  — aceptar() propaga la visita a todos sus hijos.

    Según el diagrama UML, Armario.aceptar() implementa:
        for each hijo in hijos:
            hijo.aceptar(unVisitor)
    """

    def __init__(self, nombre: str = "Armario"):
        super().__init__()
        self.nombre = nombre

    def aceptar(self, visitador) -> None:
        """
        Patrón Visitor: propaga la visita a todos los hijos.
        No llama a ningún método visitarArmario; el visitador
        recorre el contenido del armario, no el armario en sí.
        """
        for hijo in self._hijos:
            hijo.aceptar(visitador)

    def entrar(self, alguien):
        """Alguien abre el armario (accede a su contenido)."""
        print(f"  {alguien} abre {self}")
        alguien.posicion = self

    def __str__(self):
        return f"Armario({self.nombre})"
