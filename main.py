"""
Programa principal - Demostración de los patrones Factory Method, Decorator, Strategy y Composite.
"""
from juego import Juego
from orientacion import Norte, Sur, Este, Oeste
from bicho import Bicho
from modo import Agresivo, Perezoso


def main():
    """
    Función principal que demuestra el uso de los patrones
    Factory Method, Decorator y Strategy.
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
    
    # Mostrar información de las habitaciones (usa Orientacion como claves)
    print("\n3. Habitaciones del laberinto:")
    for numero, habitacion in laberinto.habitaciones.items():
        print(f"\n   {habitacion}")
        print("   Orientaciones (Strategy):")
        for orientacion, elemento in habitacion.orientaciones.items():
            print(f"      - {orientacion}: {elemento}")
    
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

    # --- Patrón Strategy: Orientacion ---
    print("\n" + "=" * 60)
    print("6. Demostración del Patrón Strategy - Orientacion:")
    print("=" * 60)

    hab = juego.fabricar_habitacion(10)
    hab.establecer_lado(Norte(), juego.fabricar_pared())
    hab.establecer_lado(Sur(), juego.fabricar_puerta())
    hab.establecer_lado(Este(), juego.fabricar_pared())
    hab.establecer_lado(Oeste(), juego.fabricar_pared())

    print(f"\n{hab}:")
    for orientacion, elemento in hab.orientaciones.items():
        print(f"  {orientacion} -> {elemento}")

    print(f"\nObtener lado Sur: {hab.obtener_lado(Sur())}")

    # --- Patrón Strategy: Modo ---
    print("\n" + "=" * 60)
    print("7. Demostración del Patrón Strategy - Modo (Bicho):")
    print("=" * 60)

    bicho = Bicho("Goblin", Agresivo())
    print(f"\n{bicho}")
    bicho.actuar()

    print("\nCambiando modo a Perezoso...")
    bicho.establecer_modo(Perezoso())
    print(f"{bicho}")
    bicho.actuar()

    print("\n" + "=" * 60)
    print("Fin de la demostración")
    print("=" * 60)


def _imprimir_arbol(elemento, nivel=0):
    """Recorre recursivamente el árbol Composite e imprime su estructura."""
    prefijo = "   " * nivel + ("+-- " if nivel > 0 else "")
    print(f"{prefijo}{elemento}")
    for hijo in elemento.obtener_hijos():
        _imprimir_arbol(hijo, nivel + 1)


def demo_composite():
    """Demuestra el patrón Composite sobre la estructura del laberinto."""
    print("\n" + "=" * 60)
    print("8. Demostración del Patrón Composite:")
    print("=" * 60)

    juego = Juego()
    laberinto = juego.crear_laberinto()

    # Mostrar el árbol Composite completo
    print("\nArbol Composite del laberinto:")
    _imprimir_arbol(laberinto)

    # Navegar con obtener_hijos() desde el laberinto
    print("\nHijos directos del Laberinto (Contenedor):")
    for hijo in laberinto.obtener_hijos():
        print(f"  {hijo}  [tipo: {type(hijo).__name__}, padre: {hijo.padre}]")

    # Navegar hijos de la primera habitación
    hab1 = laberinto.obtener_habitacion(1)
    print(f"\nHijos de {hab1} (Contenedor):")
    for hijo in hab1.obtener_hijos():
        print(f"  {hijo}  [tipo: {type(hijo).__name__}, hijos: {hijo.obtener_hijos()}]")

    # Verificar que las hojas no admiten hijos
    from pared import Pared
    pared = Pared()
    print("\nIntentando agregar hijo a una Hoja (Pared):")
    try:
        pared.agregar_hijo(juego.fabricar_pared())
    except TypeError as e:
        print(f"  Error esperado -> {e}")

    print("\n" + "=" * 60)
    print("Fin demostración Composite")
    print("=" * 60)


if __name__ == "__main__":
    main()
    demo_composite()
