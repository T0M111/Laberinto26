"""
Clase Habitacion - Elemento concreto del mapa.
"""
from elemento_mapa import ElementoMapa


class Habitacion(ElementoMapa):
    """
    Representa una habitación en el laberinto.
    Puede contener puertas y paredes en sus lados.
    """
    
    def __init__(self, numero_habitacion=0):
        """
        Inicializa una habitación.
        
        Args:
            numero_habitacion: Identificador único de la habitación.
        """
        self.numero = numero_habitacion
        self.lados = {}  # Diccionario para almacenar los lados (Norte, Sur, Este, Oeste)
    
    def establecer_lado(self, direccion, elemento):
        """
        Establece un elemento (Pared, Puerta) en un lado de la habitación.
        
        Args:
            direccion: Dirección del lado (ej: 'Norte', 'Sur', 'Este', 'Oeste')
            elemento: ElementoMapa a colocar en ese lado.
        """
        self.lados[direccion] = elemento
    
    def obtener_lado(self, direccion):
        """
        Obtiene el elemento en un lado específico.
        
        Args:
            direccion: Dirección del lado.
            
        Returns:
            El elemento en ese lado o None si no existe.
        """
        return self.lados.get(direccion)
    
    def __str__(self):
        """Representación en string de la habitación."""
        return f"Habitacion #{self.numero}"
