"""
Programa principal - Demostración de los patrones Factory Method, Decorator,
Strategy, Composite, Iterator, Template Method, Abstract Factory, Singleton,
Builder, Adapter y Navegación del laberinto.
"""
from juego import Juego
from orientacion import Norte, Sur, Este, Oeste
from bicho import Bicho
from modo import Agresivo, Perezoso
from laberinto_bombas_factory import LaberintoBombasFactory
from laberinto_fuego_factory import LaberintoFuegoFactory
from laberinto_builder import LaberintoBuilder
from director import Director
from bicho_adapter import BichoAdapter
from personaje import Personaje


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

    # --- Patrón Template Method ---
    print("\n" + "=" * 60)
    print("7b. Demostración del Patrón Template Method (GoF):")
    print("=" * 60)

    print("\nModo.actua() es el Template Method que llama:")
    print("  1. ataca(bicho)  - redefinido en Agresivo")
    print("  2. duerme(bicho) - redefinido en Perezoso")

    print("\nBicho en modo Agresivo (ataca redefinido, duerme hook):")
    bicho.establecer_modo(Agresivo())
    bicho.actuar()

    print("\nBicho en modo Perezoso (ataca hook, duerme redefinido):")
    bicho.establecer_modo(Perezoso())
    bicho.actuar()

    print("\n" + "=" * 60)
    print("Fin de la demostración")
    print("=" * 60)

    # --- Patrón Abstract Factory ---
    print("\n" + "=" * 60)
    print("8. Demostración del Patrón Abstract Factory:")
    print("=" * 60)

    juego = Juego()

    print("\n8a. Laberinto con LaberintoBombasFactory:")
    laberinto_bombas = juego.crear_laberinto(LaberintoBombasFactory())
    for numero, habitacion in laberinto_bombas.habitaciones.items():
        print(f"\n   {habitacion}")
        for orientacion, elemento in habitacion.orientaciones.items():
            print(f"      - {orientacion}: {elemento}")

    print("\n8b. Laberinto con LaberintoFuegoFactory:")
    laberinto_fuego = juego.crear_laberinto(LaberintoFuegoFactory())
    for numero, habitacion in laberinto_fuego.habitaciones.items():
        print(f"\n   {habitacion}")
        for orientacion, elemento in habitacion.orientaciones.items():
            print(f"      - {orientacion}: {elemento}")

    print("\n" + "=" * 60)
    print("Fin de la demostración completa")
    print("=" * 60)

    # --- Patrón Singleton ---
    print("\n" + "=" * 60)
    print("9. Demostración del Patrón Singleton (Norte):")
    print("=" * 60)

    n1 = Norte()
    n2 = Norte()
    n3 = Norte()
    print(f"\nn1 = Norte(): {n1}  id={id(n1)}")
    print(f"n2 = Norte(): {n2}  id={id(n2)}")
    print(f"n3 = Norte(): {n3}  id={id(n3)}")
    print(f"\nn1 is n2: {n1 is n2}")
    print(f"n2 is n3: {n2 is n3}")
    print(f"Norte.unicaInstancia is n1: {Norte.unicaInstancia is n1}")

    # --- Patrón Builder ---
    print("\n" + "=" * 60)
    print("10. Demostración del Patrón Builder:")
    print("=" * 60)

    builder = LaberintoBuilder()
    director = Director(builder)
    laberinto_builder = director.procesar()

    print(f"\nLaberinto construido por Director+LaberintoBuilder: {laberinto_builder}")
    for numero, habitacion in laberinto_builder.habitaciones.items():
        print(f"\n   {habitacion}")
        for orientacion, elemento in habitacion.orientaciones.items():
            print(f"      - {orientacion}: {elemento}")

    print("\n" + "=" * 60)
    print("Fin de la demostración")
    print("=" * 60)

    # --- Patrón Adapter ---
    print("\n" + "=" * 60)
    print("11. Demostración del Patrón Adapter (BichoAdapter):")
    print("=" * 60)

    bicho_adaptar = Bicho("Dragon", Agresivo())
    print(f"\nBicho original: {bicho_adaptar}")

    adapter = BichoAdapter(bicho_adaptar)
    mago = Personaje("Mago", adapter)

    print(f"\nPersonaje '{mago.nombre}' usa BichoAdapter como Varita.")
    print(f"Estado inicial del Bicho: {bicho_adaptar}")

    print("\nRonda 1: Personaje pide cambiar modo (Agresivo -> Perezoso):")
    mago.pedir_cambio_modo()
    print(f"  Estado tras cambio: {bicho_adaptar}")

    print("\nRonda 2: Personaje pide cambiar modo (Perezoso -> Agresivo):")
    mago.pedir_cambio_modo()
    print(f"  Estado tras cambio: {bicho_adaptar}")

    print("\nEl Personaje solo interactúa con la interfaz Varita (cambiarModo).")
    print("BichoAdapter traduce esa llamada a Bicho.cambiarModo() -> Modo.cambiarModo().")

    print("\n" + "=" * 60)
    print("Fin de la demostración del Adapter")
    print("=" * 60)

    # --- Navegación del laberinto ---
    print("\n" + "=" * 60)
    print("12. Navegación del laberinto (entrar / camina):")
    print("=" * 60)

    juego_nav = Juego()
    lab = juego_nav.crear_laberinto()

    bicho_nav = Bicho("Orco", Agresivo())

    # Colocar el bicho en la habitacion 1
    h1_nav = juego_nav.obtener_habitacion(1)
    h2_nav = juego_nav.obtener_habitacion(2)
    h1_nav.entrar(bicho_nav)
    print(f"  Posicion inicial: {bicho_nav.posicion}")

    print("\n  Intento de movimiento aleatorio con puerta cerrada:")
    bicho_nav.modo.camina(bicho_nav)
    print(f"  Posicion: {bicho_nav.posicion}")

    # Abrir la puerta entre h1 y h2
    puerta_nav = h1_nav.obtener_lado(Este())
    puerta_nav.abrir()
    print("\n  Puerta Este abierta. Movimientos aleatorios:")
    for i in range(4):
        bicho_nav.modo.camina(bicho_nav)
        print(f"  Posicion: {bicho_nav.posicion}")

    print("\n" + "=" * 60)
    print("Fin de la demostración de Navegación")
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


def demo_iterator():
    """Demuestra el patrón Iterator sobre la estructura del laberinto."""
    print("\n" + "=" * 60)
    print("9. Demostración del Patrón Iterator:")
    print("=" * 60)

    juego = Juego()
    laberinto = juego.crear_laberinto()

    # --- Iterador interno: recorrer() como generador ---
    print("\nIterador interno - recorrer() pre-order sobre el laberinto:")
    for elemento in laberinto.recorrer():
        tipo = type(elemento).__name__
        print(f"  {tipo}: {elemento}")

    # --- Iterador externo: protocolo __iter__ de Python ---
    print("\nIterador externo - `for elem in laberinto` (via __iter__):")
    tipos = [type(e).__name__ for e in laberinto]
    print(f"  Elementos recorridos: {tipos}")

    # --- Filtrar solo hojas (Pared / Puerta) ---
    print("\nSolo hojas (Pared y Puerta) dentro del laberinto:")
    from hoja import Hoja
    for elem in laberinto:
        if isinstance(elem, Hoja):
            print(f"  {elem}  [padre: {elem.padre}]")

    # --- Iterador sobre una habitacion concreta ---
    hab1 = laberinto.obtener_habitacion(1)
    print(f"\nIterando sobre {hab1} individualmente:")
    for elem in hab1:
        print(f"  {type(elem).__name__}: {elem}")

    print("\n" + "=" * 60)
    print("Fin demostración Iterator")
    print("=" * 60)


def demo_mediator():
    """Demuestra el patrón Mediator: Juego coordina Bicho y Personaje."""
    import os
    from laberinto_json_builder import LaberintoJsonBuilder

    print("\n" + "=" * 60)
    print("15. Demostración del Patrón Mediator (Juego / Bicho / Personaje):")
    print("=" * 60)

    # --- Construir laberinto y entidades desde JSON ---
    config = os.path.join(os.path.dirname(__file__), "laberinto_config.json")
    builder = LaberintoJsonBuilder(config)
    juego_med = Juego()
    Director(builder).procesar()
    builder.fabricar_entidades(juego_med)

    personaje = juego_med.personaje
    goblin = juego_med.bichos[0]
    troll  = juego_med.bichos[1]

    print(f"\nPersonaje  : {personaje.nombre} | vidas={personaje.vidas} | poder={personaje.poder}")
    for b in juego_med.bichos:
        print(f"Bicho      : {b.nombre} | vidas={b.vidas} | poder={b.poder} | modo={b.modo}")

    # --- Colocar al goblin y al personaje en la misma habitación ---
    lab = builder.fabricarLaberinto()
    hab1 = lab.obtener_habitacion(1)
    goblin.posicion   = hab1
    personaje.posicion = hab1

    print("\n--- Turno 1: Goblin ataca al Personaje (misma habitación) ---")
    juego_med.turno_bicho(goblin)

    print("\n--- Turno 2: Personaje contraataca al Goblin ---")
    juego_med.turno_personaje(goblin)

    print("\n--- Turno 3: Personaje elimina al Goblin ---")
    resultado = juego_med.turno_personaje(goblin)

    print("\n--- Turno 4: Personaje ataca al Troll (varios turnos hasta victoria) ---")
    resultado = None
    while resultado is None and troll.esta_vivo():
        resultado = juego_med.turno_personaje(troll)

    print("\nEl Mediador (Juego) coordinó todas las interacciones:")
    print("  Bicho y Personaje nunca se llamaron entre sí directamente.")
    print("  Condición de fin: victoria (todos los bichos derrotados).")

    print("=" * 60)
    print("Fin demostración Mediator")
    print("=" * 60)


def demo_prototype():
    """Demuestra el patrón Prototype: Juego clona su laberinto."""
    import os
    from laberinto_json_builder import LaberintoJsonBuilder
    from laberinto_cuadrado import LaberintoCuadrado
    from laberinto_rombiforme import LaberintoRombiforme

    print("\n" + "=" * 60)
    print("16. Demostración del Patrón Prototype (Juego / Laberinto):")
    print("=" * 60)

    config = os.path.join(os.path.dirname(__file__), "laberinto_config.json")
    builder = LaberintoJsonBuilder(config)
    juego = Juego()
    Director(builder).procesar()
    juego.laberinto = builder.fabricarLaberinto()

    print(f"\nLaberinto original : {juego.laberinto}")
    print(f"Tipo               : {type(juego.laberinto).__name__}")

    clon = juego.clonarLaberinto()
    print(f"\nClon obtenido      : {clon}")
    print(f"Tipo del clon      : {type(clon).__name__}")
    print(f"¿Es el mismo objeto? {juego.laberinto is clon}")

    # Modificar el clon no afecta al original
    from habitacion_cuadrada import HabitacionCuadrada
    clon.agregar_habitacion(HabitacionCuadrada(99))
    print(f"\nTras añadir hab 99 al clon:")
    print(f"  Original tiene {len(juego.laberinto.habitaciones)} habitaciones")
    print(f"  Clon tiene     {len(clon.habitaciones)} habitaciones")

    print("\nEl Prototipo (Laberinto) se clona a sí mismo;")
    print("Juego nunca crea habitaciones manualmente — delega en clone().")

    print("\n" + "=" * 60)
    print("Fin demostración Prototype")
    print("=" * 60)


def demo_bridge():
    """Demuestra el patrón Bridge: Forma desacoplada de Habitacion."""
    import os
    from forma import Cuadrado, Rombo
    from habitacion_cuadrada import HabitacionCuadrada
    from habitacion_rombiforme import HabitacionRombiforme
    from laberinto_json_builder import LaberintoJsonBuilder

    print("\n" + "=" * 60)
    print("14. Demostración del Patrón Bridge (Forma / Habitacion):")
    print("=" * 60)

    # --- Implementors independientes ---
    print("\nImplementors (Forma):")
    print(f"  {Cuadrado()}")
    print(f"  {Rombo()}")

    # --- Refined Abstractions directas ---
    print("\nRefined Abstractions creadas directamente:")
    hc = HabitacionCuadrada(10)
    hr = HabitacionRombiforme(11)
    print(f"  {hc}  -> forma: {hc.forma}")
    print(f"  {hr}  -> forma: {hr.forma}")

    print(f"\n  Lados de {hc}:")
    for ori, elem in hc.orientaciones.items():
        print(f"    {ori}: {elem}")

    print(f"\n  Lados de {hr}:")
    for ori, elem in hr.orientaciones.items():
        print(f"    {ori}: {elem}")

    # --- Construcción desde JSON (Builder) ---
    print("\nConstrucción desde laberinto_config.json (Builder + Bridge):")
    config = os.path.join(os.path.dirname(__file__), "laberinto_config.json")
    lab = Director(LaberintoJsonBuilder(config)).procesar()

    hab1 = lab.obtener_habitacion(1)
    print(f"  Habitación 1 del JSON: {hab1}  [tipo: {type(hab1).__name__}]")
    tunel = hab1.obtener_lado(Norte())
    hab3 = tunel.laberinto.obtener_habitacion(3)
    print(f"  Habitación 3 (laberinto secundario): {hab3}  [tipo: {type(hab3).__name__}]")
    print(f"  Forma de hab3: {hab3.forma}")

    print("\nEl Bridge desacopla la jerarquía de Habitacion de la de Forma:")
    print("  Abstraction  : Contenedor (+forma)")
    print("  Refined Abs. : HabitacionCuadrada, HabitacionRombiforme")
    print("  Implementor  : Forma")
    print("  Conc. Impl.  : Cuadrado (N/S/E/O), Rombo (NE/NO/SE/SO)")

    print("\n" + "=" * 60)
    print("Fin demostración Bridge")
    print("=" * 60)


def demo_proxy():
    """Demuestra el patrón Proxy: Tunel como proxy de Laberinto."""
    import os
    from tunel import Tunel
    from laberinto_json_builder import LaberintoJsonBuilder

    print("\n" + "=" * 60)
    print("13. Demostración del Patrón Proxy (Tunel):")
    print("=" * 60)

    # --- Construcción desde JSON (requisito Builder) ---
    config = os.path.join(os.path.dirname(__file__), "laberinto_config.json")
    builder = LaberintoJsonBuilder(config)
    director = Director(builder)
    lab_principal = director.procesar()

    print(f"\nLaberinto construido desde JSON: {lab_principal}")
    for numero, habitacion in lab_principal.habitaciones.items():
        print(f"\n   {habitacion}")
        for orientacion, elemento in habitacion.orientaciones.items():
            print(f"      - {orientacion}: {elemento}")

    # --- El Tunel como lado de la Habitacion 1 ---
    hab1 = lab_principal.obtener_habitacion(1)
    tunel = hab1.obtener_lado(Norte())
    print(f"\nLado Norte de Habitación 1 es: {tunel}  [tipo: {type(tunel).__name__}]")
    print(f"Laberinto al que apunta: {tunel.laberinto}")

    # --- El bicho entra al túnel: teletransporte ---
    bicho_proxy = Bicho("Explorador", Perezoso())
    hab1.entrar(bicho_proxy)
    print(f"\n{bicho_proxy.nombre} está en: {bicho_proxy.posicion}")

    print(f"\n{bicho_proxy.nombre} intenta entrar por el Norte (Tunel):")
    tunel.entrar(bicho_proxy)
    print(f"  Ahora está en: {bicho_proxy.posicion}  <- laberinto secundario")

    print("\nEl Tunel (Proxy) delegó entrar() en el Laberinto real sin que")
    print("el Bicho supiera que cruzó a otro laberinto.")

    print("\n" + "=" * 60)
    print("Fin demostración Proxy")
    print("=" * 60)


def demo_prototype():
    """Demuestra el patrón Prototype: Juego clona su laberinto."""
    import os
    from laberinto_json_builder import LaberintoJsonBuilder
    from laberinto_cuadrado import LaberintoCuadrado
    from habitacion_cuadrada import HabitacionCuadrada

    print("\n" + "=" * 60)
    print("16. Demostración del Patrón Prototype (Juego / Laberinto):")
    print("=" * 60)

    config = os.path.join(os.path.dirname(__file__), "laberinto_config.json")
    builder = LaberintoJsonBuilder(config)
    juego_proto = Juego()
    Director(builder).procesar()
    juego_proto.laberinto = builder.fabricarLaberinto()

    print(f"\nLaberinto original : {juego_proto.laberinto}")
    print(f"Tipo               : {type(juego_proto.laberinto).__name__}")

    clon = juego_proto.clonarLaberinto()
    print(f"\nClon obtenido      : {clon}")
    print(f"Tipo del clon      : {type(clon).__name__}")
    print(f"¿Es el mismo objeto? {juego_proto.laberinto is clon}")

    # Modificar el clon no afecta al original
    clon.agregar_habitacion(HabitacionCuadrada(99))
    print(f"\nTras añadir hab 99 al clon:")
    print(f"  Original tiene {len(juego_proto.laberinto.habitaciones)} habitaciones")
    print(f"  Clon tiene     {len(clon.habitaciones)} habitaciones")

    print("\nEl Prototipo (Laberinto) se clona a sí mismo;")
    print("Juego.clonarLaberinto() delega en laberinto.clone().")

    print("\n" + "=" * 60)
    print("Fin demostración Prototype")
    print("=" * 60)


def demo_observer():
    """Demuestra el patrón Observer: Juego (Subject) notifica a LaberintoGUI (Observer)."""
    import os
    from laberinto_json_builder import LaberintoJsonBuilder
    from laberinto_gui import LaberintoGUI
    from personaje import Personaje

    print("\n" + "=" * 60)
    print("17. Demostración del Patrón Observer (Juego / LaberintoGUI):")
    print("=" * 60)

    # Construir juego con laberinto desde JSON
    config = os.path.join(os.path.dirname(__file__), "laberinto_config.json")
    builder = LaberintoJsonBuilder(config)
    juego_obs = Juego()
    Director(builder).procesar()
    juego_obs.laberinto = builder.fabricarLaberinto()
    builder.fabricar_entidades(juego_obs)

    # Crear y suscribir la GUI como observadora
    gui = LaberintoGUI()
    juego_obs.suscribir(gui)
    print("\nLaberintoGUI suscrita al Juego como observadora.")
    print(f"Observadores activos: {len(juego_obs._observadores)}")

    # Un ataque dispara la notificación automáticamente
    personaje = juego_obs.personaje
    if juego_obs.bichos:
        bicho = juego_obs.bichos[0]
        print(f"\n[Ataque] {bicho.nombre} ataca a {personaje.nombre}...")
        juego_obs.notificar_ataque(bicho, personaje)

    # Desuscribir y comprobar que la GUI ya no recibe notificaciones
    juego_obs.desuscribir(gui)
    print(f"\nGUI desuscrita. Observadores activos: {len(juego_obs._observadores)}")
    print("Próxima notificación no llegará a la GUI.")

    print("\n" + "=" * 60)
    print("Fin demostración Observer")
    print("=" * 60)


def demo_command():
    """Demuestra el patrón Command: Puerta con comandos Abrir y Cerrar."""
    from puerta import Puerta
    from abrir import Abrir
    from cerrar import Cerrar

    print("\n" + "=" * 60)
    print("18. Demostración del Patrón Command (Puerta / Abrir / Cerrar):")
    print("=" * 60)

    puerta = Puerta()
    print(f"\nPuerta inicial   : {puerta}")
    print(f"Comandos disponibles: {[type(c).__name__ for c in puerta.comandos]}")

    print("\n[Invoker] Ejecutando Abrir...")
    puerta.comandos[0].ejecutar()
    print(f"  Estado puerta  : {puerta}")

    print("\n[Invoker] Ejecutando Cerrar...")
    puerta.comandos[1].ejecutar()
    print(f"  Estado puerta  : {puerta}")

    print("\nTambién se pueden crear comandos independientes:")
    cmd_abrir = Abrir(puerta)
    cmd_abrir.ejecutar()
    print(f"  Abrir directo  : {puerta}")

    print("\n" + "=" * 60)
    print("Fin demostración Command")
    print("=" * 60)


def demo_visitor():
    """Demuestra el patrón Visitor: VisitadorContador recorre el laberinto."""
    import os
    from laberinto_json_builder import LaberintoJsonBuilder
    from visitador_contador import VisitadorContador
    from armario import Armario
    from pared import Pared
    from puerta import Puerta

    print("\n" + "=" * 60)
    print("19. Demostración del Patrón Visitor (Laberinto / VisitadorContador):")
    print("=" * 60)

    # Construir laberinto desde JSON
    config = os.path.join(os.path.dirname(__file__), "laberinto_config.json")
    builder = LaberintoJsonBuilder(config)
    Director(builder).procesar()
    lab = builder.fabricarLaberinto()

    # Recorrer con el Visitador Contador
    vc = VisitadorContador()
    lab.aceptar(vc)
    print(f"\nLaberinto analizado : {lab}")
    print(f"Resultado           : {vc}")

    # Añadir un Armario con objetos y recorrer de nuevo
    armario = Armario("Tesoro")
    armario.agregar_hijo(Pared())
    armario.agregar_hijo(Puerta())
    hab = list(lab.habitaciones.values())[0]
    hab.agregar_hijo(armario)

    vc2 = VisitadorContador()
    lab.aceptar(vc2)
    print(f"\nTras añadir Armario('Tesoro') con Pared + Puerta a hab #{hab.numero}:")
    print(f"  {vc2}")
    print(f"  (El Armario propaga la visita a sus hijos sin contarse a sí mismo)")

    print("\n" + "=" * 60)
    print("Fin demostración Visitor")
    print("=" * 60)


def demo_flyweight():
    """Demuestra el patrón Flyweight: FactoriaMonedas comparte instancias de Moneda."""
    from laberinto import Laberinto
    from habitacion import Habitacion
    from orientacion import Norte, Sur, Este, Oeste
    from pared import Pared

    print("\n" + "=" * 60)
    print("20. Demostración del Patrón Flyweight (Moneda / FactoriaMonedas):")
    print("=" * 60)

    lab = Laberinto()
    h1 = Habitacion(1)
    h2 = Habitacion(2)
    lab.agregar_habitacion(h1)
    lab.agregar_habitacion(h2)

    f = lab.factoria_monedas

    # Obtener flyweights: misma instancia para la misma clave
    oro1 = f.getMoneda("oro")
    oro2 = f.getMoneda("oro")
    plata = f.getMoneda("plata")
    super_m = f.getMoneda("super_moneda")

    print(f"\nFactoria tiene {len(f)} instancias en pool (crea solo una por tipo):")
    for m in f.monedas:
        print(f"  {type(m).__name__}: value={m.value}")

    print(f"\noro1 is oro2 (misma instancia): {oro1 is oro2}")
    print(f"oro1 is plata (instancias distintas): {oro1 is plata}")

    # Estado extrínseco: posicion cambia sin crear nuevos objetos
    oro1.posicion = h1
    plata.posicion = h2
    super_m.posicion = h1
    print(f"\nEstado extrínseco (posicion) — sin crear objetos nuevos:")
    for m in f.monedas:
        print(f"  {m}")

    print("\n" + "=" * 60)
    print("Fin demostración Flyweight")
    print("=" * 60)


if __name__ == "__main__":
    main()
    demo_composite()
    demo_iterator()
    demo_bridge()
    demo_proxy()
    demo_mediator()
    demo_prototype()
    demo_observer()
    demo_command()
    demo_visitor()
    demo_flyweight()
