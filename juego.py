"""
Clase Juego - Factory Method, Abstract Factory, Mediator, cliente Prototype y Subject Observer.

Patón Observer (Subject):
  - Subject          : Juego   (este fichero)
  - Observer         : Observador   (observador.py)
  - ConcreteObserver : LaberintoGUI (laberinto_gui.py)
  Juego notifica a todos sus observadores cada vez que el estado del juego cambia.

Patón Prototype (cliente):
  - Client    : Juego.clonarLaberinto()  — clona el laberinto activo
  - Prototype : Laberinto.clone()

Patrón Mediator:
  - Mediator   : Juego  (este fichero)
  - ColleagueA : Bicho
  - ColleagueB : Personaje
  Juego coordina las interacciones entre Bichos y Personaje sin que
  éstos se conozcan directamente, y verifica las condiciones de fin de juego.
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

    def __init__(self):
        """Inicializa el Juego sin laberinto ni entidades activas."""
        self.laberinto = None
        # --- Mediator ---
        self.personaje = None  # Colleague B: el Personaje del jugador
        self.bichos = []       # Colleague A: lista de Bichos activos
        # --- Observer (Subject) ---
        self._observadores = []  # lista de Observador suscritos
        # --- Chain of Responsibility (Client) ---
        self.handler = None   # primer ElementoMapa de la cadena (+handler 1)
    
    def obtener_habitacion(self, numero):
        """
        Delega en el laberinto activo la búsqueda de una habitación por número.

        Args:
            numero: Número de la habitación.

        Returns:
            La Habitacion correspondiente, o None si no existe o no hay laberinto.
        """
        if self.laberinto is None:
            return None
        return self.laberinto.obtener_habitacion(numero)

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

        # Establecer los lados de la puerta
        puerta.lado1 = h1
        puerta.lado2 = h2

        # Agregar habitaciones al laberinto
        laberinto.agregar_habitacion(h1)
        laberinto.agregar_habitacion(h2)

        self.laberinto = laberinto
        return laberinto

    # =========================================================================
    # Patrón Mediator — coordinación entre Bicho y Personaje
    # =========================================================================

    def registrar_personaje(self, personaje):
        """
        Registra el Personaje como Colleague B del Mediador.
        Establece la referencia bidireccional (_juego).

        Args:
            personaje: Instancia de Personaje.
        """
        self.personaje = personaje
        personaje._juego = self

    def registrar_bicho(self, bicho):
        """
        Registra un Bicho como Colleague A del Mediador.
        Establece la referencia bidireccional (_juego).

        Args:
            bicho: Instancia de Bicho.
        """
        self.bichos.append(bicho)
        bicho._juego = self

    def notificar_ataque(self, atacante, objetivo):
        """
        Mediador: aplica el daño de 'atacante' a 'objetivo' y comprueba
        las condiciones de fin de juego.
        Ningún Colleague llama directamente al otro; todo pasa por aquí.

        Args:
            atacante: Ente que realiza el ataque.
            objetivo: Ente que recibe el daño.

        Returns:
            Resultado de verificar_fin_juego() ('victoria'|'derrota'|None).
        """
        objetivo.recibir_danio(atacante.poder)
        print(f"  {atacante.nombre} ataca a {objetivo.nombre}! "
              f"[{objetivo.nombre}: {objetivo.vidas} vidas, estado: {objetivo.estado}]")
        resultado = self.verificar_fin_juego()
        self.notificar()  # Observer: avisa a todos los observadores
        return resultado

    def turno_bicho(self, bicho):
        """
        Mediador: orquesta el turno de un Bicho.
        Si el Bicho y el Personaje están en la misma habitación → ataca.
        En caso contrario → el Bicho actúa según su Modo (se mueve).

        Args:
            bicho: El Bicho cuyo turno se ejecuta.

        Returns:
            Resultado de verificar_fin_juego() si hubo ataque, si no None.
        """
        if not bicho.esta_vivo():
            print(f"  {bicho.nombre} está eliminado y no puede actuar.")
            return None
        misma_habitacion = (
            self.personaje is not None
            and self.personaje.esta_vivo()
            and bicho.posicion is not None
            and bicho.posicion is self.personaje.posicion
        )
        if misma_habitacion:
            print(f"  ¡{bicho.nombre} encuentra al Personaje en {bicho.posicion}!")
            return self.notificar_ataque(bicho, self.personaje)
        else:
            bicho.actuar()
            return None

    def turno_personaje(self, bicho_objetivo=None):
        """
        Mediador: orquesta el turno del Personaje.
        Si se especifica un bicho objetivo vivo → el personaje lo ataca.

        Args:
            bicho_objetivo: Bicho a atacar (opcional).

        Returns:
            Resultado de verificar_fin_juego() si hubo ataque, si no None.
        """
        if self.personaje is None or not self.personaje.esta_vivo():
            print("  El personaje no puede actuar.")
            return None
        if bicho_objetivo is not None and bicho_objetivo.esta_vivo():
            return self.notificar_ataque(self.personaje, bicho_objetivo)
        print(f"  {self.personaje.nombre} no tiene objetivo en rango.")
        return None

    def verificar_fin_juego(self):
        """
        Mediador: comprueba las condiciones de fin de juego.

        Condición de DERROTA : el Personaje está Muerto.
        Condición de VICTORIA: todos los Bichos están Muertos.

        Returns:
            'derrota' | 'victoria' | None (juego continúa).
        """
        if self.personaje is not None and not self.personaje.esta_vivo():
            print("\n  *** GAME OVER: El personaje ha sido derrotado. ***")
            return "derrota"
        if self.bichos and all(not b.esta_vivo() for b in self.bichos):
            print("\n  *** VICTORIA: Todos los bichos han sido derrotados. ***")
            return "victoria"
        return None

    # ------------------------------------------------------------------
    # Patrón Observer (Subject)
    # ------------------------------------------------------------------

    def suscribir(self, observador) -> None:
        """
        Registra un Observador para recibir notificaciones de este Juego.

        Args:
            observador: Instancia de Observador a suscribir.
        """
        if observador not in self._observadores:
            self._observadores.append(observador)

    def desuscribir(self, observador) -> None:
        """
        Elimina un Observador de la lista de notificaciones.

        Args:
            observador: Instancia de Observador a desuscribir.
        """
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar(self) -> None:
        """
        Notifica a todos los Observadores suscritos del cambio de estado.
        Cada observador recibe una llamada a actualizar(self).
        """
        for obs in list(self._observadores):
            obs.actualizar(self)

    # ------------------------------------------------------------------
    # Patrón Prototype (cliente)
    # ------------------------------------------------------------------

    def clonarLaberinto(self):
        """
        Patrón Prototype: delega en el laberinto activo su propio clone().
        Devuelve una copia profunda e independiente del laberinto actual.

        Returns:
            Nueva instancia del mismo tipo de laberinto con todos sus
            elementos copiados (habitaciones, puertas, paredes, etc.).

        Raises:
            ValueError: Si no hay ningún laberinto activo en el juego.
        """
        if self.laberinto is None:
            raise ValueError("No hay laberinto activo que clonar.")
        return self.laberinto.clone()

    # ------------------------------------------------------------------
    # Patrón Chain of Responsibility (Cliente)
    # ------------------------------------------------------------------

    def cerrarPuertas(self) -> None:
        """
        Patrón Chain of Responsibility — lanza la petición en la cadena.
        Delega en el primer ElementoMapa de la cadena (+handler).
        Cada Puerta de la cadena responde (cierra), las Paredes pasan.

        Raises:
            ValueError: Si no hay ningún handler configurado.
        """
        if self.handler is None:
            raise ValueError("No hay handler configurado para cerrarPuertas.")
        self.handler.cerrarPuertas()
