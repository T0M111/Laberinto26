# Modus Operandi - Flujo de Trabajo Git

## Proceso para cada Patrón de Diseño

### 1. Crear rama específica para el patrón
```bash
git checkout -b feature/nombre-del-patron
```

Ejemplos de nombres:
- `feature/factory-method`
- `feature/abstract-factory`
- `feature/builder`
- `feature/prototype`
- `feature/singleton`

### 2. Desarrollar la implementación
- Crear/modificar las clases necesarias
- Escribir código de demostración
- Actualizar README con documentación del patrón

### 3. Preparar el commit
```bash
# Agregar archivos relevantes
git add *.py README.md

# Hacer commit con mensaje descriptivo
git commit -m "feat: Implementar patrón [NOMBRE]

- Descripción de cambios principales
- Clases creadas
- Funcionalidad implementada"
```

### 4. Subir rama al repositorio remoto
```bash
git push -u origin feature/nombre-del-patron
```

### 5. Crear Pull Request
- Ir a la URL proporcionada por Git
- Crear PR hacia la rama `main`
- Revisar cambios
- Mergear cuando esté listo

### 6. Volver a main para siguiente patrón
```bash
git checkout main
git pull origin main
```

## Convenciones de nombres de commits

- `feat:` - Nueva funcionalidad (nuevo patrón)
- `fix:` - Corrección de errores
- `docs:` - Cambios en documentación
- `refactor:` - Refactorización de código
- `test:` - Agregar o modificar tests

## Estado actual

- ✅ **Factory Method** (v0.1.0) - Implementado y mergeado a `main`
  - Clases: `ElementoMapa`, `Pared`, `Puerta`, `Habitacion`, `Laberinto`, `Juego`
  - Rama: `feature/factory-method`

- ✅ **Decorator** (v0.2.0) - Implementado y mergeado a `main`
  - Clases: `Decorator`, `Bomba`, `Hechizo`
  - Rama: `feature/decorator`
  - Commits:
    - feat: Añadir clase Decorator base del patrón Decorator
    - feat: Añadir decorador concreto Bomba
    - feat: Añadir decorador concreto Hechizo

- ✅ **Strategy** (v0.3.0) - Implementado
  - Clases: `Orientacion`, `Norte`, `Sur`, `Este`, `Oeste`, `Modo`, `Agresivo`, `Perezoso`, `Bicho`
  - Rama: `feature/strategy`
  - Cambios:
    - `orientacion.py`: Interfaz Strategy `Orientacion` con estrategias concretas `Norte`, `Sur`, `Este`, `Oeste`
    - `modo.py`: Interfaz Strategy `Modo` con estrategias concretas `Agresivo`, `Perezoso`
    - `bicho.py`: Clase `Bicho` que delega comportamiento en un objeto `Modo`
    - `habitacion.py`: Actualizada para usar objetos `Orientacion` como claves en lugar de strings

- ✅ **Composite** (v0.4.0) - Implementado
  - Clases: `Hoja`, `Contenedor`
  - Rama: `feature/composite`
  - Cambios:
    - `elemento_mapa.py`: Añadido atributo `+padre` e interfaz `agregar_hijo` / `eliminar_hijo` / `obtener_hijos`
    - `hoja.py`: Nueva clase abstracta `Hoja(ElementoMapa)` — nodo hoja sin hijos
    - `contenedor.py`: Nueva clase abstracta `Contenedor(ElementoMapa)` — nodo compuesto con `+padre` y `+hijos`
    - `pared.py`: `Pared` ahora extiende `Hoja`
    - `puerta.py`: `Puerta` ahora extiende `Hoja`
    - `laberinto.py`: `Laberinto` ahora extiende `Contenedor`; `agregar_habitacion` registra también como hijo Composite
    - `habitacion.py`: `Habitacion` ahora extiende `Contenedor`; `establecer_lado` registra el elemento como hijo Composite

- ✅ **Iterator** (v0.5.0) - Implementado
  - Rama: `feature/iterator`
  - Cambios:
    - `elemento_mapa.py`: Añadido método abstracto `+recorrer()` e `__iter__` que delega en él
    - `hoja.py`: `Hoja.recorrer()` — generador que solo produce `self` (nodo terminal)
    - `contenedor.py`: `Contenedor.recorrer()` — generador pre-order que produce `self` y recursa en cada hijo con `yield from`
    - Iterador interno: uso directo de `elemento.recorrer()`
    - Iterador externo: uso con `for elem in elemento` vía protocolo `__iter__`

- ✅ **Template Method** (v0.6.0) - Implementado
  - Referencia: *Design Patterns: Elements of Reusable Object-Oriented Software* (GoF)
  - Rama: `feature/template-method`
  - Cambios:
    - `modo.py`: `Modo.actua()` es ahora el Template Method que define el esqueleto del algoritmo llamando a `ataca()` y `duerme()`; métodos primitivos con implementación por defecto (hooks) redefinidos en subclases
    - `Agresivo`: redefine `ataca()` con comportamiento agresivo
    - `Perezoso`: redefine `duerme()` con comportamiento perezoso
    - `bicho.py`: `Bicho.actuar()` ahora invoca `modo.actua(self)` (Template Method)
    - Se eliminó el método abstracto `ejecutar()` en favor del Template Method `actua()`

## Versionado

- ✅ **Abstract Factory** (v0.7.0) - Implementado
  - Rama: `feature/abstract-factory`
  - Cambios:
    - `laberinto_factory.py`: Clase abstracta `LaberintoFactory` (ABC) con `fabricar_pared()` y `fabricar_puerta()` abstractos
    - `pared_bomba.py`: `ParedBomba(Pared)` — producto concreto de pared con bomba
    - `pared_fuego.py`: `ParedFuego(Pared)` — producto concreto de pared de fuego
    - `puerta_bomba.py`: `PuertaBomba(Puerta)` — producto concreto de puerta con bomba
    - `puerta_fuego.py`: `PuertaFuego(Puerta)` — producto concreto de puerta de fuego
    - `laberinto_bombas_factory.py`: `LaberintoBombasFactory(LaberintoFactory)` — factoría que produce `ParedBomba` + `PuertaBomba`
    - `laberinto_fuego_factory.py`: `LaberintoFuegoFactory(LaberintoFactory)` — factoría que produce `ParedFuego` + `PuertaFuego`
    - `juego.py`: `crear_laberinto(factory=None)` acepta una `LaberintoFactory` opcional; si se pasa, delega la creación de paredes/puertas en ella

- ✅ **Singleton** (v0.8.0) - Implementado
  - Rama: `feature/singleton`
  - Cambios:
    - `orientacion.py`: `Norte` implementa el patrón Singleton mediante `__new__`; el atributo de clase `unicaInstancia` almacena la única instancia y cualquier llamada a `Norte()` la devuelve en lugar de crear una nueva

- ✅ **Builder** (v0.9.0) - Implementado
  - Rama: `feature/builder`
  - Cambios:
    - `builder.py`: Clase abstracta `Builder` (ABC) con método abstracto `fabricarLaberinto()`
    - `laberinto_builder.py`: `LaberintoBuilder(Builder)` — builder concreto que ensambla un `Laberinto` con dos habitaciones conectadas por una puerta
    - `director.py`: `Director` — almacena un `Builder` en `self.builder` y su método `procesar()` delega en `builder.fabricarLaberinto()`

- ✅ **Adapter** (v1.0.0) - Implementado
  - Rama: `feature/adapter`
  - Cambios:
    - `varita.py`: Clase abstracta `Varita` (Target) con método abstracto `cambiarModo()`
    - `bicho_adapter.py`: `BichoAdapter(Varita)` — Adapter concreto que envuelve un `Bicho` (adaptee) y delega `cambiarModo()` en `bicho.cambiarModo()`
    - `personaje.py`: `Personaje` — Cliente que solo conoce la interfaz `Varita`; invoca `varita.cambiarModo()` para cambiar el modo del bicho sin referenciarlo directamente
    - `bicho.py`: Añadido método `cambiarModo()` — delega en `modo.cambiarModo(self)` (doble despacho)
    - `modo.py`: Añadido método abstracto `cambiarModo(bicho)` en `Modo`; `Agresivo.cambiarModo()` transiciona a `Perezoso`, `Perezoso.cambiarModo()` transiciona a `Agresivo`

- ✅ **Navegación del Laberinto** (v1.1.0) - Implementado
  - Rama: `feature/navegacion`
  - Cambios:
    - `elemento_mapa.py`: Añadidos hooks `entrar(alguien)` (bloqueado por defecto) y `caminar(alguien)` (delega en `entrar`) sobre los que cada subclase hace polimorfismo
    - `contenedor.py`: `Contenedor.entrar(alguien)` — imprime posición y asigna `alguien.posicion = self`
    - `habitacion.py`: `Habitacion.obtener_orientacion_aleatoria()` — devuelve un `ElementoMapa` aleatorio de `orientaciones.values()` (equivalente a `detect:` de Smalltalk)
    - `puerta.py`: Añadidos atributos `lado1` y `lado2`; `Puerta.entrar(alguien)` — si abierta, mueve al bicho al lado contrario; si cerrada, imprime mensaje
    - `bicho.py`: Añadido atributo `posicion = None`
    - `modo.py`: `Modo.camina(bicho)` — obtiene elemento aleatorio de la posición del bicho y llama `elemento.caminar(bicho)`
    - `juego.py`: Añadido `__init__` con `self.laberinto = None`; `crear_laberinto()` asigna `puerta.lado1/lado2` y almacena el laberinto en `self.laberinto`; nuevo método `obtener_habitacion(num)` que delega en `self.laberinto.obtener_habitacion(num)`
    - `laberinto.py`: `obtener_habitacion(num)` ahora itera `_hijos` con `next(filter(...), None)` (fiel al `detect:ifNone:` del profesor)

## Versionado

- `v0.1.0` - Factory Method
- `v0.2.0` - Decorator
- `v0.3.0` - Strategy
- `v0.4.0` - Composite
- `v0.5.0` - Iterator
- `v0.6.0` - Template Method
- `v0.7.0` - Abstract Factory
- `v0.8.0` - Singleton
- `v0.9.0` - Builder
- `v1.0.0` - Adapter
- `v1.1.0` - Navegación del Laberinto
- `v1.2.0` - Proxy (Tunel)
- `v1.3.0` - Bridge (Forma / HabitacionCuadrada / HabitacionRombiforme)
- `v1.4.0` - Mediator (Juego coordina Bicho / Personaje a través de Ente)
- `v1.5.0` - State (Estado / Vivo / Muerto aplicado al ciclo de vida de Ente)
- `v1.6.0` - Prototype (LaberintoCuadrado / LaberintoRombiforme; Juego.clonarLaberinto())
- `v1.7.0` - Observer (Juego como Subject; LaberintoGUI como ConcreteObserver)
- `v1.8.0` - Command (Abrir / Cerrar sobre Puerta; ElementoMapa con +comandos)
- `v1.9.0` - Visitor (Visitador ABC; VisitadorContador; +aceptar() en ElementoMapa; nuevo Armario)

---

## Extensiones de Evaluación

- ✅ **Proxy** (v1.2.0) — extensión Media
  - Rama: `feature/proxy`
  - Patrón: Proxy
  - Roles:
    - Subject: `ElementoMapa` (interfaz `entrar()`)
    - RealSubject: `Laberinto`
    - Proxy: `Tunel`
  - Nuevos ficheros:
    - `tunel.py`: `Tunel(Contenedor)` — proxy que teletransporta al ente a la primera habitación del laberinto destino
    - `laberinto_config.json`: configuración JSON con dos laberintos y un túnel entre ellos
    - `laberinto_json_builder.py`: `LaberintoJsonBuilder(Builder)` — builder basado en JSON que soporta `pared`, `puerta`, `tunel`
    - `test_tunel.py`: 13 tests (Tunel + LaberintoJsonBuilder)
  - `main.py`: añadida `demo_proxy()` (sección 13)

- ✅ **Bridge** (v1.3.0) — extensión Media
  - Rama: `feature/bridge`
  - Patrón: Bridge
  - Roles:
    - Abstraction: `Contenedor` (recibe `+forma: Forma`)
    - Refined Abstractions: `HabitacionCuadrada`, `HabitacionRombiforme`
    - Implementor: `Forma` (abstracta, `+num`, `+orientaciones`)
    - Concrete Implementors: `Cuadrado` (N/S/E/O), `Rombo` (NE/NO/SE/SO)
  - Nuevos ficheros:
    - `forma.py`: `Forma` (ABC), `Cuadrado`, `Rombo`
    - `habitacion_cuadrada.py`: `HabitacionCuadrada(Habitacion)` — inicializa sus 4 lados cardinales con Pared
    - `habitacion_rombiforme.py`: `HabitacionRombiforme(Habitacion)` — inicializa sus 4 lados diagonales con Pared
    - `test_bridge.py`: 24 tests (Forma + HabitacionCuadrada + HabitacionRombiforme + integración JSON)
  - Ficheros modificados:
    - `orientacion.py`: añadidas `Noreste`, `Noroeste`, `Sureste`, `Suroeste`
    - `contenedor.py`: añadido `self.forma = None` en `__init__`
    - `laberinto_config.json`: habitaciones 1 y 2 son `habitacion_cuadrada`; habitación 3 es `habitacion_rombiforme`
    - `laberinto_json_builder.py`: soporta `habitacion`, `habitacion_cuadrada`, `habitacion_rombiforme`; soporta orientaciones diagonales
  - `main.py`: añadida `demo_bridge()` (sección 14)

- ✅ **Mediator** (v1.4.0) — extensión Media
  - Rama: `feature/mediator`
  - Patrón: Mediator
  - Roles:
    - Mediador: `Juego` — coordina ataques, condiciones de fin de juego y registro de entidades
    - Colegas: `Bicho` y `Personaje` — se comunican **solo a través de Juego**, nunca entre sí
    - Colleague Base: `Ente` (abstracta) — encapsula `vidas`, `poder`, `estado` y referencia `_juego`
    - State: `Estado` (abstracta), `Vivo`, `Muerto` — patrón State para el ciclo de vida del Ente
  - Nuevos ficheros:
    - `estado_ente.py`: `Estado` (ABC), `Vivo`, `Muerto` — patrón State (refactorizado en v1.5.0 como patrón independiente)
    - `ente.py`: `Ente` (ABC) — clase base Colega con `vidas`, `poder`, `estado`, `_juego`, `recibir_danio()`, `esta_vivo()`
    - `test_mediator.py`: 40 tests (Estado/State + Ente + Bicho/Personaje como Ente + Juego Mediador + fabricar_entidades)
  - Ficheros modificados:
    - `bicho.py`: `Bicho(Ente)` — ahora hereda de `Ente`; constructor backwards-compatible `(nombre, modo, vidas=3, poder=1)`
    - `personaje.py`: `Personaje(Ente)` — ahora hereda de `Ente`; `varita` ahora opcional; `(nombre, varita=None, vidas=5, poder=2)`
    - `juego.py`: añadidos `self.personaje`, `self.bichos`; métodos Mediador: `registrar_personaje()`, `registrar_bicho()`, `notificar_ataque()`, `turno_bicho()`, `turno_personaje()`, `verificar_fin_juego()`
    - `laberinto_config.json`: añadida sección `"entidades"` con Heroe, Goblin y Troll
    - `laberinto_json_builder.py`: añadido método `fabricar_entidades(juego)` que lee la sección JSON y registra las entidades en el Juego
  - `main.py`: añadida `demo_mediator()` (sección 15)

- ✅ **State** (v1.5.0) — extensión Básica
  - Rama: `feature/state`
  - Patrón: State
  - Roles:
    - Context        : `Ente` — tiene `+estado: Estado` y delega `actuar()` en `estado.puedeActuar()`
    - State          : `Estado` (ABC) — define `puedeActuar() -> bool`
    - ConcreteState A: `Vivo` — `puedeActuar()` devuelve `True`
    - ConcreteState B: `Muerto` — `puedeActuar()` devuelve `False`
  - Ficheros modificados:
    - `estado_ente.py`: renombrado `EstadoEnte` → `Estado`; renombrado `esta_vivo()` → `puedeActuar()`
    - `ente.py`: importa `Estado`; `actuar()` delega en `self.estado.puedeActuar()`; `esta_vivo()` como alias de conveniencia
    - `bicho.py`: `actuar()` llama `super().actuar()` como guardia State antes de ejecutar Strategy (retorna el bool)
  - Nuevos ficheros:
    - `test_state.py`: 19 tests (TestEstado + TestEnteComoContextoState + TestBichoConStateguard)

- ✅ **Prototype** (v1.6.0) — extensión Básica
  - Rama: `feature/prototype`
  - Patrón: Prototype
  - Roles:
    - Prototype          : `Laberinto` — define `clone()` usando `copy.deepcopy`
    - ConcretePrototype A: `LaberintoCuadrado` — sobrescribe `clone()`, devuelve `LaberintoCuadrado`
    - ConcretePrototype B: `LaberintoRombiforme` — sobrescribe `clone()`, devuelve `LaberintoRombiforme`
    - Client             : `Juego.clonarLaberinto()` — delega en `self.laberinto.clone()`
  - Nuevos ficheros:
    - `laberinto_cuadrado.py`: `LaberintoCuadrado(Laberinto)` con `clone()` y `__str__`
    - `laberinto_rombiforme.py`: `LaberintoRombiforme(Laberinto)` con `clone()` y `__str__`
    - `test_prototype.py`: 23 tests (TestLaberintoClone + TestLaberintoCuadradoClone + TestLaberintoRombiformeClone + TestJuegoComoClientePrototype + TestJsonBuilderCreaLaberintosTipados)
  - Ficheros modificados:
    - `laberinto.py`: añadido `clone()` (Prototype) e importado `copy`
    - `juego.py`: añadido `clonarLaberinto()` como método cliente del Prototype
    - `laberinto_config.json`: añadido campo `"tipo"` en cada laberinto (`laberinto_cuadrado` / `laberinto_rombiforme`)
    - `laberinto_json_builder.py`: importa `LaberintoCuadrado`/`LaberintoRombiforme`; tabla `_TIPOS_LABERINTO`; primera pasada usa el tipo correcto
  - `main.py`: añadida `demo_prototype()` (sección 16)

- ✅ **Observer** (v1.7.0) — extensión Media
  - Rama: `feature/observer`
  - Patrón: Observer (variante Pull — el ConcreteObserver recibe el Subject y extrae lo que necesita)
  - Roles:
    - Subject            : `Juego` — mantiene `_observadores: list`; métodos `suscribir()`, `desuscribir()`, `notificar()`
    - Observer           : `Observador` (ABC) — define `actualizar(juego) -> None`
    - ConcreteObserver   : `LaberintoGUI` — referencia de vuelta `+juego`; `actualizar()` actualiza `self.juego` y llama `_mostrar_estado()`
  - Nuevos ficheros:
    - `observador.py`: `Observador(ABC)` con método abstracto `actualizar(self, juego) -> None`
    - `laberinto_gui.py`: `LaberintoGUI(Observador)` — muestra vidas/estado del Personaje y los Bichos, e indica resultado (Victoria / Derrota / en curso)
    - `test_observer.py`: 21 tests (TestObservadorAbstracto + TestJuegoSubject + TestLaberintoGUI)
  - Ficheros modificados:
    - `juego.py`: añadido `self._observadores = []` en `__init__`; métodos `suscribir()`, `desuscribir()`, `notificar()`; `notificar_ataque()` llama `self.notificar()` automáticamente al final de cada ataque
  - `main.py`: añadida `demo_observer()` (sección 17)

- ✅ **Command** (v1.8.0) — extensión Media
  - Rama: `feature/command`
  - Patrón: Command
  - Roles:
    - Command            : `Comando` (ABC) — `+receptor`; método abstracto `ejecutar()`
    - ConcreteCommand A  : `Abrir` — `ejecutar()` llama `receptor.abrir()`
    - ConcreteCommand B  : `Cerrar` — `ejecutar()` llama `receptor.cerrar()`
    - Receiver           : `Puerta` — posee los métodos `abrir()` y `cerrar()`
    - Invoker/Client     : `ElementoMapa` — lista `+comandos` (0..*); `Puerta` se auto-registra con Abrir y Cerrar
  - Nuevos ficheros:
    - `comando.py`: `Comando(ABC)` con `self.receptor` y método abstracto `ejecutar() -> None`
    - `abrir.py`: `Abrir(Comando)` — ConcreteCommand que abre la puerta
    - `cerrar.py`: `Cerrar(Comando)` — ConcreteCommand que cierra la puerta
    - `test_command.py`: 23 tests (TestComandoAbstracto + TestAbrir + TestCerrar + TestElementoMapaComandos + TestPuertaConComandos)
  - Ficheros modificados:
    - `elemento_mapa.py`: añadido `self.comandos = []` en `__init__`
    - `puerta.py`: importa `Abrir` y `Cerrar`; `__init__` inicializa `self.comandos = [Abrir(self), Cerrar(self)]`
  - `main.py`: añadida `demo_command()` (sección 18)

- ✅ **Visitor** (v1.9.0) — extensión Avanzada
  - Rama: `feature/visitor`
  - Patrón: Visitor (doble despacho: cada ElementoMapa llama al método visit correspondiente)
  - Roles:
    - Visitor            : `Visitador` (ABC) — define `visitarHabitacion()`, `visitarPuerta()`, `visitarPared()`
    - ConcreteVisitor    : `VisitadorContador` — cuenta elementos por tipo (habitaciones / puertas / paredes)
    - Element (abstract) : `ElementoMapa` — nuevo método abstracto `+aceptar(Visitor)`
    - ConcreteElement    : `Habitacion` — `aceptar()` llama `visitarHabitacion(self)` y propaga a los hijos
    - ConcreteElement    : `Puerta` — `aceptar()` llama `visitarPuerta(self)` (doble despacho)
    - ConcreteElement    : `Pared` — `aceptar()` llama `visitarPared(self)` (doble despacho)
    - Container base     : `Contenedor` — `aceptar()` generico: itera hijos (usado por Laberinto, Tunel, Armario)
    - Nuevo Contenedor   : `Armario` — `aceptar()` propaga a hijos sin llamar a visitarArmario (según diagrama UML)
  - Nuevos ficheros:
    - `visitador.py`: `Visitador(ABC)` con los tres métodos abstractos de visita
    - `visitador_contador.py`: `VisitadorContador(Visitador)` — contadores de habitaciones / puertas / paredes
    - `armario.py`: `Armario(Contenedor)` — nuevo contenedor con `aceptar()` de propagación y `entrar()`
    - `test_visitor.py`: 25 tests (TestVisitadorAbstracto + TestDobleDespacho + TestHabitacionAceptar + TestArmarioAceptar + TestVisitadorContador + TestContenedorAceptarPropagacion)
  - Ficheros modificados:
    - `elemento_mapa.py`: añadido método abstracto `aceptar(visitador) -> None`
    - `contenedor.py`: añadida implementación base `aceptar()` — itera `_hijos` (heredada por Laberinto, Tunel, Armario)
    - `habitacion.py`: sobrescribe `aceptar()` — `visitarHabitacion(self)` + propagación a hijos
    - `puerta.py`: sobrescribe `aceptar()` — `visitarPuerta(self)`
    - `pared.py`: sobrescribe `aceptar()` — `visitarPared(self)`
    - Subclases concretas (ParedBomba, PuertaFuego, HabitacionCuadrada, etc.) heredan `aceptar()` correctamente sin cambios
  - `main.py`: añadida `demo_visitor()` (sección 19)
