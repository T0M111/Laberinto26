"""
Clase Puerta - Hoja concreta del mapa (Composite).
"""
from hoja import Hoja
from abrir import Abrir
from cerrar import Cerrar


class Puerta(Hoja):
    """
    Representa una puerta en el laberinto.
    Es un elemento hoja que conecta dos habitaciones; no contiene hijos.
    """

    def __init__(self):
        """Inicializa una puerta."""
        super().__init__()
        self.abierta = False
        self.lado1 = None  # Primera habitacion conectada
        self.lado2 = None  # Segunda habitacion conectada
        # Patrón Command: comandos disponibles sobre esta puerta
        self.comandos = [Abrir(self), Cerrar(self)]
    
    def abrir(self):
        """Abre la puerta."""
        self.abierta = True
    
    def cerrar(self):
        """Cierra la puerta."""
        self.abierta = False
    
    def entrar(self, alguien):
        """
        El bicho intenta cruzar la puerta.
        Si está abierta, lo mueve a la habitacion del otro lado.
        Si está cerrada, imprime un mensaje.
        """
        if self.abierta:
            if alguien.posicion is self.lado1:
                self.lado2.entrar(alguien)
            else:
                self.lado1.entrar(alguien)
        else:
            print("  La puerta está cerrada.")

    def __str__(self):
        """Representación en string de la puerta."""
        estado = "abierta" if self.abierta else "cerrada"
        return f"Puerta ({estado})"
