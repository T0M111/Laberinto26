"""
Programa principal - Demostración del patrón Factory Method.
"""
from juego import Juego


def main():
    """
    Función principal que demuestra el uso del patrón Factory Method
    para crear un laberinto.
    """
    print("=" * 60)
    print("Demostración del Patrón Factory Method - Laberinto")
    print("=" * 60)
    
    # Crear una instancia del juego
    juego = Juego()
    
    # Usar el factory method para crear un laberinto
    print("\n1. Creando laberinto usando Factory Methods...")
    laberinto = juego.crear_laberinto()
    
    # Mostrar información del laberinto
    print(f"\n2. {laberinto}")
    
    # Mostrar información de las habitaciones
    print("\n3. Habitaciones del laberinto:")
    for numero, habitacion in laberinto.habitaciones.items():
        print(f"\n   {habitacion}")
        print("   Lados:")
        for direccion, elemento in habitacion.lados.items():
            print(f"      - {direccion}: {elemento}")
    
    # Demostrar el uso individual de los factory methods
    print("\n" + "=" * 60)
    print("4. Demostración de Factory Methods individuales:")
    print("=" * 60)
    
    pared = juego.fabricar_pared()
    print(f"\nFactory Method fabricar_pared(): {pared}")
    
    puerta = juego.fabricar_puerta()
    print(f"Factory Method fabricar_puerta(): {puerta}")
    
    habitacion = juego.fabricar_habitacion(99)
    print(f"Factory Method fabricar_habitacion(99): {habitacion}")
    
    nuevo_laberinto = juego.fabricar_laberinto()
    print(f"Factory Method fabricar_laberinto(): {nuevo_laberinto}")
    
    # Demostrar funcionalidad de la puerta
    print("\n" + "=" * 60)
    print("5. Demostración de funcionalidad de Puerta:")
    print("=" * 60)
    
    puerta_demo = juego.fabricar_puerta()
    print(f"\nPuerta inicial: {puerta_demo}")
    
    puerta_demo.abrir()
    print(f"Después de abrir: {puerta_demo}")
    
    puerta_demo.cerrar()
    print(f"Después de cerrar: {puerta_demo}")
    
    print("\n" + "=" * 60)
    print("Fin de la demostración")
    print("=" * 60)


if __name__ == "__main__":
    main()
