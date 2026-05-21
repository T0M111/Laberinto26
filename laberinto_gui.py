"""
Patrón Observer — ConcreteObserver: LaberintoGUI.

Roles:
  - Subject          : Juego        (juego.py)
  - Observer         : Observador   (observador.py)
  - ConcreteObserver : LaberintoGUI (este fichero)

LaberintoGUI mantiene una referencia (+juego) al Subject para poder
consultar su estado cuando recibe la notificación (variante pull).
Representa la interfaz gráfica/textual del laberinto: muestra el estado
del juego cada vez que Juego llama a notificar().
"""
from observador import Observador


class LaberintoGUI(Observador):
    """
    ConcreteObserver del patrón Observer.
    Recibe notificaciones de Juego y presenta el estado actual del juego
    de forma textual (simula una GUI).

    Atributos:
        juego : referencia al Subject (Juego) — back-reference para pull.
    """

    def __init__(self, juego=None):
        """
        Args:
            juego: Instancia de Juego a observar (opcional;
                   también se puede asignar al suscribir).
        """
        self.juego = juego  # back-reference al Subject (+juego del diagrama)

    def actualizar(self, juego) -> None:
        """
        Notificación pull: Juego avisa de que su estado ha cambiado.
        LaberintoGUI consulta el estado directamente a través de 'juego'
        y lo muestra por pantalla.

        Args:
            juego: El Subject que emite la notificación.
        """
        self.juego = juego  # actualiza la referencia por si cambió
        self._mostrar_estado()

    def _mostrar_estado(self):
        """Presenta el estado actual del juego (simulación de GUI)."""
        juego = self.juego
        print("\n  [LaberintoGUI] ── Estado del juego ──────────────────────")

        # Personaje
        if juego.personaje is not None:
            p = juego.personaje
            estado_str = str(p.estado)
            print(f"    Personaje : {p.nombre}  vidas={p.vidas}  [{estado_str}]")

        # Bichos
        for b in juego.bichos:
            estado_str = str(b.estado)
            print(f"    Bicho     : {b.nombre}  vidas={b.vidas}  [{estado_str}]")

        # Resultado
        resultado = juego.verificar_fin_juego()
        if resultado == "derrota":
            print("    >>> FIN: Derrota <<<")
        elif resultado == "victoria":
            print("    >>> FIN: Victoria <<<")
        else:
            print("    >>> Juego en curso <<<")
        print("  ────────────────────────────────────────────────────────")
