# Laberinto26 - Patrón Factory Method

Proyecto de ejemplo que implementa el patrón de diseño **Factory Method** para la creación de un laberinto.

## Descripción

Este proyecto demuestra la implementación del patrón Factory Method aplicado a la construcción de un laberinto. El patrón permite encapsular la creación de objetos, delegando a las subclases la responsabilidad de decidir qué clase instanciar.

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
├── main.py              # Programa principal de demostración
└── README.md            # Este archivo
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
