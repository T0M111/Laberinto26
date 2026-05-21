"""
Clase abstracta Ente — Context del patrón State y Colleague del patrón Mediator.

Roles del patrón State:
  - Context : Ente                  (este fichero)
  - State   : Estado                (estado_ente.py)

Roles del patrón Mediator:
  - Mediator   : Juego
  - Colleague  : Ente  (clase abstracta)
  - ColleagueA : Bicho
  - ColleagueB : Personaje

Ente.actuar() delega en self.estado.puedeActuar() (State pattern).
Ente mantiene también una referencia al Mediador (_juego) para notificar
eventos sin acoplarse directamente al resto de colegas.
"""
from abc import ABC, abstractmethod
from estado_ente import Estado, Vivo, Muerto


class Ente(ABC):
    """
    Context del patrón State y Colleague abstracto del patrón Mediator.

    Atributos:
        vidas  (int)    : puntos de vida actuales.
        poder  (int)    : daño que inflige por ataque.
        estado (Estado) : estado actual (Vivo / Muerto) — State pattern.
        _juego          : referencia al Mediador; lo asigna Juego al registrar.
    """

    def __init__(self, vidas: int = 3, poder: int = 1):
        if vidas <= 0:
            raise ValueError(f"Las vidas deben ser > 0, recibido: {vidas}")
        if poder <= 0:
            raise ValueError(f"El poder debe ser > 0, recibido: {poder}")
        self.vidas: int = vidas
        self.poder: int = poder
        self.estado: Estado = Vivo()
        self._juego = None  # Mediador; se asigna al registrar en Juego

    # ------------------------------------------------------------------
    # Patrón State
    # ------------------------------------------------------------------

    def actuar(self) -> bool:
        """
        Patrón State: delega en el estado actual para saber si el ente
        puede llevar a cabo una acción (estado→puedeActuar()).

        Las subclases deben llamar a super().actuar() como guardia antes
        de ejecutar su comportamiento específico.

        Returns:
            True si el ente puede actuar (estado Vivo),
            False en caso contrario (estado Muerto).
        """
        return self.estado.puedeActuar()

    # ------------------------------------------------------------------
    # Gestión de vida
    # ------------------------------------------------------------------

    def recibir_danio(self, cantidad: int) -> None:
        """
        Reduce las vidas del ente. Si llegan a 0 la transición de estado
        es Vivo → Muerto (State pattern).

        Args:
            cantidad: Puntos de daño recibidos (debe ser > 0).
        """
        if cantidad <= 0:
            raise ValueError(f"El daño debe ser > 0, recibido: {cantidad}")
        self.vidas = max(0, self.vidas - cantidad)
        if self.vidas == 0:
            self.estado = Muerto()

    def esta_vivo(self) -> bool:
        """Conveniencia: True si el estado actual permite actuar."""
        return self.estado.puedeActuar()

    @abstractmethod
    def __str__(self) -> str:
        pass
