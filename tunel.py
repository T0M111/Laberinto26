"""
Clase Tunel - Patrón Proxy.

Roles del patrón:
  - Subject     : ElementoMapa  (interfaz común con entrar/recorrer)
  - RealSubject : Laberinto     (el laberinto al que el túnel da acceso)
  - Proxy       : Tunel         (este fichero)

El Tunel puede colocarse como lado de una Habitacion (igual que Pared o Puerta).
Al invocar entrar(), delega en el Laberinto real y teletransporta al personaje
a su primera habitación.
"""
from contenedor import Contenedor


class Tunel(Contenedor):
    """
    Proxy del patrón Proxy.

    Atributos:
        laberinto (Laberinto): referencia al RealSubject (+laberinto, cardinalidad 1).
    """

    def __init__(self, laberinto):
        """
        Inicializa el Tunel con una referencia al Laberinto destino.

        Args:
            laberinto: Instancia de Laberinto a la que el túnel da acceso.

        Raises:
            ValueError: si laberinto es None.
        """
        if laberinto is None:
            raise ValueError("Tunel requiere un Laberinto destino (no puede ser None)")
        super().__init__()
        self.laberinto = laberinto  # +laberinto : Laberinto  [1]

    def entrar(self, alguien):
        """
        Proxy: delega la navegación en el Laberinto real.
        Transporta a 'alguien' a la primera habitación del laberinto destino.

        Args:
            alguien: El ente (Bicho/Personaje) que intenta entrar.
        """
        print(f"  {alguien} entra en el túnel... ¡TELETRANSPORTE!")
        habitaciones = list(self.laberinto.habitaciones.values())
        if not habitaciones:
            raise RuntimeError(
                f"El laberinto destino '{self.laberinto}' no tiene habitaciones"
            )
        # Delegación al RealSubject: el personaje aparece en la primera habitación
        habitaciones[0].entrar(alguien)

    def __str__(self):
        return f"Tunel -> {self.laberinto}"
