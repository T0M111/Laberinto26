"""
Clase Juego - Implementa el patrón Factory Method.
"""
from pared import Pared
from puerta import Puerta
from habitacion import Habitacion
from laberinto import Laberinto


class Juego:
    """
    Clase que implementa los Factory Methods para crear elementos del laberinto.
    
    Esta clase encapsula la creación de los diferentes elementos del mapa
    (Pared, Puerta, Habitacion, Laberinto) permitiendo que subclases puedan
    sobrescribir estos métodos para crear variantes de los elementos.
    """
    
    def fabricar_pared(self):
        """
        Factory Method para crear una Pared.
        
        Returns:
            Una nueva instancia de Pared.
        """
        return Pared()
    
    def fabricar_puerta(self):
        """
        Factory Method para crear una Puerta.
        
        Returns:
            Una nueva instancia de Puerta.
        """
        return Puerta()
    
    def fabricar_habitacion(self, numero=0):
        """
        Factory Method para crear una Habitacion.
        
        Args:
            numero: Número identificador de la habitación.
            
        Returns:
            Una nueva instancia de Habitacion.
        """
        return Habitacion(numero)
    
    def fabricar_laberinto(self):
        """
        Factory Method para crear un Laberinto.
        
        Returns:
            Una nueva instancia de Laberinto.
        """
        return Laberinto()
    
    def crear_laberinto(self):
        """
        Método que utiliza los Factory Methods para construir un laberinto completo.
        Este es un ejemplo de cómo usar los factory methods.
        
        Returns:
            Un laberinto configurado con dos habitaciones conectadas por una puerta.
        """
        # Crear el laberinto
        laberinto = self.fabricar_laberinto()
        
        # Crear dos habitaciones
        h1 = self.fabricar_habitacion(1)
        h2 = self.fabricar_habitacion(2)
        
        # Crear elementos para las habitaciones
        puerta = self.fabricar_puerta()
        
        # Configurar la habitación 1
        h1.establecer_lado("Norte", self.fabricar_pared())
        h1.establecer_lado("Este", puerta)
        h1.establecer_lado("Sur", self.fabricar_pared())
        h1.establecer_lado("Oeste", self.fabricar_pared())
        
        # Configurar la habitación 2
        h2.establecer_lado("Norte", self.fabricar_pared())
        h2.establecer_lado("Este", self.fabricar_pared())
        h2.establecer_lado("Sur", self.fabricar_pared())
        h2.establecer_lado("Oeste", puerta)
        
        # Agregar habitaciones al laberinto
        laberinto.agregar_habitacion(h1)
        laberinto.agregar_habitacion(h2)
        
        return laberinto
