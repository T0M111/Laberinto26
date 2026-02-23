"""
Patrón Strategy + Template Method - Modo de comportamiento de un Bicho.
Clase abstracta Modo y sus estrategias concretas: Agresivo, Perezoso.

El método actua() es un Template Method (GoF - Design Patterns: Elements of
Reusable Object-Oriented Software) que define el esqueleto del algoritmo de
comportamiento, delegando los pasos concretos ataca() y duerme() a las
subclases.
"""
from abc import ABC, abstractmethod


class Modo(ABC):
    """
    Clase abstracta que combina Strategy + Template Method.
    - Strategy: Bicho delega su comportamiento en un objeto Modo intercambiable.
    - Template Method: actua() define el esqueleto del algoritmo y llama a los
      métodos primitivos ataca() y duerme(), que cada subclase redefine.
    """

    # --- Template Method ---

    def actua(self, bicho):
        """
        Template Method (GoF).
        Define el algoritmo general de comportamiento de un Bicho.
        Llama a los métodos primitivos ataca() y duerme(), cuya
        implementación concreta depende de la subclase.

        Args:
            bicho: El Bicho que actúa según este modo.
        """
        self.ataca(bicho)
        self.duerme(bicho)

    # --- Métodos primitivos (hooks) ---

    def ataca(self, bicho):
        """
        Paso del template method: atacar.
        Implementación por defecto: no hace nada (hook).
        Redefinido en Agresivo.
        """
        pass

    def duerme(self, bicho):
        """
        Paso del template method: dormir.
        Implementación por defecto: no hace nada (hook).
        Redefinido en Perezoso.
        """
        pass

    @abstractmethod
    def obtener_nombre(self):
        """Devuelve el nombre del modo."""
        pass

    def __str__(self):
        return self.obtener_nombre()


class Agresivo(Modo):
    """Estrategia concreta: el bicho ataca activamente."""

    def obtener_nombre(self):
        return "Agresivo"

    def ataca(self, bicho):
        """Paso concreto del Template Method: ataque agresivo."""
        print(f"  {bicho} -> ¡Ataca ferozmente!")


class Perezoso(Modo):
    """Estrategia concreta: el bicho descansa sin hacer nada."""

    def obtener_nombre(self):
        return "Perezoso"

    def duerme(self, bicho):
        """Paso concreto del Template Method: duerme profundamente."""
        print(f"  {bicho} -> Duerme profundamente... zzz")
