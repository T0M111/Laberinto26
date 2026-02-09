# Laberinto26 - Patrones de Diseño

Proyecto de ejemplo que implementa múltiples patrones de diseño aplicados a la creación y decoración de un laberinto.

## Patrones Implementados

- ✅ **Factory Method** (v0.1.0) - Creación de elementos del laberinto
- ✅ **Decorator** (v0.2.0) - Agregar funcionalidades dinámicas a elementos

## Descripción

Este proyecto demuestra la implementación de patrones de diseño aplicados a la construcción de un laberinto:

1. **Factory Method**: Encapsula la creación de objetos del laberinto
2. **Decorator**: Permite agregar funcionalidades (bombas, hechizos) a elementos existentes sin modificar su estructura

## Estructura del Proyecto

```
Laberinto26/
│
├── elemento_mapa.py     # Clase abstracta base para todos los elementos
├── pared.py             # Clase concreta: Pared
├── puerta.py            # Clase concreta: Puerta  
├── habitacion.py        # Clase concreta: Habitación
├── laberinto.py         # Clase concreta: Laberinto
├── juego.py             # Clase con Factory Methods
├── decorator.py         # Decorador base (patrón Decorator)
├── bomba.py             # Decorador concreto: Bomba
├── hechizo.py           # Decorador concreto: Hechizo
├── main.py              # Programa principal de demostración
├── README.md            # Este archivo
└── WORKFLOW.md          # Flujo de trabajo Git
```

## Clases Principales

### ElementoMapa (Clase Abstracta)
Clase base abstracta para todos los elementos del laberinto.

### Clases Concretas
- **Pared**: Representa una pared que bloquea el paso
- **Puerta**: Representa una puerta que conecta habitaciones (puede estar abierta o cerrada)
- **Habitacion**: Representa una habitación con 4 lados (Norte, Sur, Este, Oeste)
- **Laberinto**: Contenedor de todas las habitaciones

### Juego (Factory)
Implementa los Factory Methods:
- `fabricar_pared()`: Crea instancias de Pared
- `fabricar_puerta()`: Crea instancias de Puerta
- `fabricar_habitacion(numero)`: Crea instancias de Habitacion
- `fabricar_laberinto()`: Crea instancias de Laberinto
- `crear_laberinto()`: Método que utiliza los factory methods para construir un laberinto completo

## Patrón Factory Method

El patrón Factory Method:
- Define una interfaz para crear objetos
- Permite que las subclases decidan qué clase instanciar
- Delega la instanciación a métodos específicos
- Facilita la extensibilidad y el mantenimiento del código

## Patrón Decorator

El patrón Decorator:
- Permite agregar responsabilidades adicionales a objetos dinámicamente
- Proporciona una alternativa flexible a la herencia para extender funcionalidad
- Los decoradores tienen la misma interfaz que los objetos que envuelven
- Se pueden apilar múltiples decoradores sobre un mismo objeto

### Decoradores Implementados

- **Decorator**: Clase base que envuelve un `ElementoMapa` y delega operaciones
- **Bomba**: Decorador que añade capacidad explosiva (estados: activa/explotada)
- **Hechizo**: Decorador que añade efectos mágicos (estados: activo/usado)

### Ejemplo de Uso

```python
# Decorar una habitación con una bomba
habitacion = Habitacion(1)
habitacion_con_bomba = Bomba(habitacion)

# Decorar una puerta con un hechizo
puerta = Puerta()
puerta_con_hechizo = Hechizo(puerta)

# Apilar decoradores
elemento = Hechizo(Bomba(Pared()))
```

## Ejecución

Para ejecutar el programa de demostración:

```bash
python main.py
```

## Extensibilidad

Este diseño permite fácilmente:
- Crear variantes de elementos (ej: ParedReforzada, PuertaMagica)
- Extender la clase Juego para crear diferentes tipos de laberintos
- Agregar nuevos tipos de elementos sin modificar el código existente

## Autor

Proyecto desarrollado para la asignatura de Diseño de Software
