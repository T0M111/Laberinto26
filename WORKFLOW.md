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

- `v0.1.0` - Factory Method
- `v0.2.0` - Decorator
- `v0.3.0` - Strategy
- `v0.4.0` - Composite
- `v0.5.0` - Iterator
- `v0.6.0` - Template Method
