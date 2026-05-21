"""
Clase Laberinto - Contenedor concreto del mapa (Composite) y Prototype.

Patrón Prototype:
  - Prototype          : Laberinto  (define clone())
  - ConcretePrototype A: LaberintoCuadrado   (laberinto_cuadrado.py)
  - ConcretePrototype B: LaberintoRombiforme (laberinto_rombiforme.py)
  - Client             : Juego.clonarLaberinto()

Patrón Flyweight (cliente):
  - Client             : Laberinto  (posee +factoria_monedas: FactoriaMonedas)

Patrón Memento (Originator):
  - Originator         : Laberinto  (+estado, crearMemento(), cargarPartida())
"""
import copy
from contenedor import Contenedor
from factoria_monedas import FactoriaMonedas
from memento import Memento


class Laberinto(Contenedor):
    """
    Representa el laberinto completo.
    Contenedor de nivel superior: sus hijos directos son Habitacion.
    Extiende Contenedor del patrón Composite.

    Actúa además como Prototype: define clone() que las subclases concretas
    deben sobrescribir para devolver una copia profunda de sí mismas.
    """

    def __init__(self):
        """Inicializa el laberinto."""
        super().__init__()
        self.habitaciones = {}  # Acceso rápido por número (mantiene compatibilidad)
        self.factoria_monedas = FactoriaMonedas()  # Patrón Flyweight

    def agregar_habitacion(self, habitacion):
        """
        Agrega una habitación al laberinto.
        La registra en el dict y también como hijo Composite.

        Args:
            habitacion: Objeto Habitacion a agregar.
        """
        self.habitaciones[habitacion.numero] = habitacion
        self.agregar_hijo(habitacion)

    def obtener_habitacion(self, numero):
        """
        Obtiene una habitación por su número recorriendo los hijos Composite
        (equivalente al detect:ifNone: del profesor en Smalltalk).

        Args:
            numero: Número de la habitación.

        Returns:
            La habitación correspondiente o None si no existe.
        """
        return next(
            (h for h in self._hijos if hasattr(h, 'numero') and h.numero == numero),
            None
        )

    def clone(self):
        """
        Patrón Prototype: devuelve una copia profunda del laberinto.
        Las subclases ConcretePrototype (LaberintoCuadrado, LaberintoRombiforme)
        sobrescriben este método para garantizar el tipo correcto.

        Returns:
            Una copia independiente de este laberinto.
        """
        return copy.deepcopy(self)

    # ------------------------------------------------------------------
    # Patrón Memento (Originator)
    # ------------------------------------------------------------------

    @property
    def estado(self):
        """
        Patrón Memento: estado actual del laberinto.
        Representa la colección de habitaciones que define la estructura del mapa.
        """
        return self.habitaciones

    def crearMemento(self) -> Memento:
        """
        Patrón Memento: crea un snapshot del estado actual.
        Guarda una copia profunda de las habitaciones para que el Caretaker
        pueda custodiarlo sin depender del Laberinto original.

        Returns:
            Memento con una copia profunda del estado actual.
        """
        return Memento(copy.deepcopy(self.habitaciones))

    def cargarPartida(self, m: Memento) -> None:
        """
        Patrón Memento: restaura el estado desde un Memento.
        Reemplaza las habitaciones actuales por las del snapshot
        y reconstruye la lista de hijos Composite.

        Args:
            m: Memento que contiene el estado a restaurar.
        """
        estado = m.getEstado()
        self.habitaciones = estado
        self._hijos = list(estado.values())
        for hab in self._hijos:
            hab.padre = self

    def __str__(self):
        """Representación en string del laberinto."""
        return f"Laberinto con {len(self.habitaciones)} habitaciones"
