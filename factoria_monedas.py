"""
Patrón Flyweight — FactoriaMonedas (Flyweight Factory).

Gestiona un pool de instancias de Moneda compartidas.
getMoneda(key) devuelve siempre la misma instancia para la misma clave,
evitando crear objetos duplicados con el mismo estado intrínseco.

Claves soportadas: "oro", "plata", "super_moneda"
"""
from oro import Oro
from plata import Plata
from super_moneda import SuperMoneda


class FactoriaMonedas:
    """
    Patrón Flyweight — FlyweightFactory.

    Mantiene el pool +monedas (1..*) de instancias compartidas de Moneda.
    El cliente (Laberinto) usa getMoneda(key) para obtener la flyweight
    y luego establece el estado extrínseco (posicion) desde fuera.

    Atributos:
        _pool (dict): mapa {key -> Moneda} — instancias compartidas.

    Claves válidas:
        "oro"         → Oro       (value=10)
        "plata"       → Plata     (value=5)
        "super_moneda"→ SuperMoneda (value=50)
    """

    _TIPOS = {
        "oro": Oro,
        "plata": Plata,
        "super_moneda": SuperMoneda,
    }

    def __init__(self):
        self._pool = {}  # +monedas: pool de flyweights compartidos

    def getMoneda(self, key: str):
        """
        Devuelve la instancia compartida de Moneda para la clave dada.
        Si todavía no existe en el pool, la crea y la almacena.

        Args:
            key: identificador del tipo de moneda ("oro", "plata", "super_moneda").

        Returns:
            Instancia de Moneda compartida correspondiente a la clave.

        Raises:
            ValueError: si la clave no corresponde a ningún tipo conocido.
        """
        if key not in self._TIPOS:
            raise ValueError(
                f"Tipo de moneda desconocido: '{key}'. "
                f"Válidos: {list(self._TIPOS)}"
            )
        if key not in self._pool:
            self._pool[key] = self._TIPOS[key]()
        return self._pool[key]

    @property
    def monedas(self):
        """Devuelve la lista de flyweights actualmente en el pool (+monedas 1..*)."""
        return list(self._pool.values())

    def __len__(self):
        return len(self._pool)
