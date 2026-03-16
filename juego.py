"""
Clase Juego - Implementa los patrones Factory Method y Abstract Factory.
Usa el patrón Strategy (Orientacion) para los lados de las habitaciones.
"""
from pared import Pared
from puerta import Puerta
from habitacion import Habitacion
from laberinto import Laberinto
from orientacion import Norte, Sur, Este, Oeste
from laberinto_factory import LaberintoFactory


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
    
    def crear_laberinto(self, factory: LaberintoFactory = None):
        """
        Crea un laberinto completo usando los Factory Methods propios
        o, si se proporciona una factoría (Abstract Factory), delega en ella
        la creación de Pared y Puerta.

        Args:
            factory: Instancia de LaberintoFactory (Abstract Factory).
                     Si es None se usan los Factory Methods de la propia clase.

        Returns:
            Un laberinto configurado con dos habitaciones conectadas por una puerta.
        """
        def _pared():
            return factory.fabricar_pared() if factory else self.fabricar_pared()

        def _puerta():
            return factory.fabricar_puerta() if factory else self.fabricar_puerta()

        # Crear el laberinto
        laberinto = self.fabricar_laberinto()
        
        # Crear dos habitaciones
        h1 = self.fabricar_habitacion(1)
        h2 = self.fabricar_habitacion(2)
        
        # Crear elementos para las habitaciones
        puerta = _puerta()
        
        # Configurar la habitación 1
        h1.establecer_lado(Norte(), _pared())
        h1.establecer_lado(Este(), puerta)
        h1.establecer_lado(Sur(), _pared())
        h1.establecer_lado(Oeste(), _pared())
        
        # Configurar la habitación 2
        h2.establecer_lado(Norte(), _pared())
        h2.establecer_lado(Este(), _pared())
        h2.establecer_lado(Sur(), _pared())
        h2.establecer_lado(Oeste(), puerta)
        
        # Agregar habitaciones al laberinto
        laberinto.agregar_habitacion(h1)
        laberinto.agregar_habitacion(h2)
        
        return laberinto
