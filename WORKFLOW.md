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

## Versionado

- `v0.1.0` - Factory Method
- `v0.2.0` - Decorator
- `v0.3.0` - Strategy
