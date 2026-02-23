"""
Clase Laberinto - Contenedor concreto del mapa (Composite).
"""
from contenedor import Contenedor


class Laberinto(Contenedor):
    """
    Representa el laberinto completo.
    Contenedor de nivel superior: sus hijos directos son Habitacion.
    Extiende Contenedor del patrón Composite.
    """

    def __init__(self):
        """Inicializa el laberinto."""
        super().__init__()
        self.habitaciones = {}  # Acceso rápido por número (mantiene compatibilidad)

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
        Obtiene una habitación por su número.

        Args:
            numero: Número de la habitación.

        Returns:
            La habitación correspondiente o None si no existe.
        """
        return self.habitaciones.get(numero)

    def __str__(self):
        """Representación en string del laberinto."""
        return f"Laberinto con {len(self.habitaciones)} habitaciones"
