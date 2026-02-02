"""
Clase Laberinto - Elemento concreto del mapa que contiene toda la estructura.
"""
from elemento_mapa import ElementoMapa


class Laberinto(ElementoMapa):
    """
    Representa el laberinto completo.
    Contiene todas las habitaciones del juego.
    """
    
    def __init__(self):
        """Inicializa el laberinto."""
        self.habitaciones = {}
    
    def agregar_habitacion(self, habitacion):
        """
        Agrega una habitación al laberinto.
        
        Args:
            habitacion: Objeto Habitacion a agregar.
        """
        self.habitaciones[habitacion.numero] = habitacion
    
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
