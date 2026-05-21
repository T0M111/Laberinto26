"""
Clase LaberintoJsonBuilder - Builder concreto dirigido por un fichero JSON.
Extiende el patrón Builder para soportar Tunel (patrón Proxy) y
HabitacionCuadrada / HabitacionRombiforme (patrón Bridge).

El fichero JSON debe seguir el esquema de laberinto_config.json:
  - "laberintos" : lista de laberintos con habitaciones y lados
  - "laberinto_raiz" : id del laberinto que se devuelve como resultado
"""
import json
import os

from builder import Builder
from laberinto import Laberinto
from habitacion import Habitacion
from habitacion_cuadrada import HabitacionCuadrada
from habitacion_rombiforme import HabitacionRombiforme
from pared import Pared
from puerta import Puerta
from tunel import Tunel
from orientacion import Norte, Sur, Este, Oeste, Noreste, Noroeste, Sureste, Suroeste


_ORIENTACIONES = {
    "norte":    Norte,
    "sur":      Sur,
    "este":     Este,
    "oeste":    Oeste,
    "noreste":  Noreste,
    "noroeste": Noroeste,
    "sureste":  Sureste,
    "suroeste": Suroeste,
}

_TIPOS_HABITACION = {
    "habitacion":            Habitacion,
    "habitacion_cuadrada":   HabitacionCuadrada,
    "habitacion_rombiforme": HabitacionRombiforme,
}


class LaberintoJsonBuilder(Builder):
    """
    Builder concreto que lee la estructura del laberinto desde un JSON
    y construye el grafo de objetos correspondiente, incluyendo Tuneles
    (Proxy) y HabitacionCuadrada/HabitacionRombiforme (Bridge).
    """

    def __init__(self, ruta_json: str):
        """
        Args:
            ruta_json: Ruta al fichero JSON de configuración.

        Raises:
            FileNotFoundError: si el fichero no existe.
            ValueError: si el JSON no tiene el formato esperado.
        """
        if not os.path.isfile(ruta_json):
            raise FileNotFoundError(f"No se encontró el fichero de configuración: {ruta_json}")
        with open(ruta_json, "r", encoding="utf-8") as f:
            self._config = json.load(f)

        if "laberintos" not in self._config or "laberinto_raiz" not in self._config:
            raise ValueError("El JSON debe contener 'laberintos' y 'laberinto_raiz'")

    def fabricarLaberinto(self):
        """
        Lee el JSON y construye el grafo completo de ElementoMapa.

        Returns:
            El Laberinto raíz completamente configurado.
        """
        # 1ª pasada: crear todos los Laberinto vacíos indexados por id
        laberintos = {}
        for spec in self._config["laberintos"]:
            laberintos[spec["id"]] = Laberinto()

        # 2ª pasada: crear habitaciones y lados (pared/puerta/tunel)
        puertas_compartidas = {}  # id_puerta -> Puerta (para compartir entre dos habitaciones)

        for spec in self._config["laberintos"]:
            lab = laberintos[spec["id"]]
            for hab_spec in spec["habitaciones"]:
                hab = self._crear_habitacion(hab_spec)
                for dir_str, lado_spec in hab_spec["lados"].items():
                    orientacion_cls = _ORIENTACIONES.get(dir_str)
                    if orientacion_cls is None:
                        raise ValueError(f"Orientación desconocida: '{dir_str}'")
                    elemento = self._crear_elemento(lado_spec, laberintos, puertas_compartidas)
                    hab.establecer_lado(orientacion_cls(), elemento)
                lab.agregar_habitacion(hab)

        raiz_id = self._config["laberinto_raiz"]
        if raiz_id not in laberintos:
            raise ValueError(f"laberinto_raiz '{raiz_id}' no está definido en 'laberintos'")
        return laberintos[raiz_id]

    # ------------------------------------------------------------------
    # Métodos auxiliares privados
    # ------------------------------------------------------------------

    def _crear_habitacion(self, hab_spec: dict):
        """
        Fábrica interna: crea la Habitacion (o subclase Bridge) apropiada.

        Si el JSON incluye "tipo", se usa el tipo especificado.
        Si no, se crea una Habitacion estándar.

        Args:
            hab_spec: Diccionario con al menos "numero".

        Raises:
            ValueError: si el tipo de habitacion es desconocido.
        """
        numero = hab_spec["numero"]
        tipo = hab_spec.get("tipo", "habitacion")
        hab_cls = _TIPOS_HABITACION.get(tipo)
        if hab_cls is None:
            raise ValueError(f"Tipo de habitacion desconocido en el JSON: '{tipo}'")
        # HabitacionCuadrada y HabitacionRombiforme inicializan sus lados
        # con paredes por defecto; el bucle exterior sobreescribe los que
        # aparecen en el JSON (llamadas a establecer_lado son idempotentes).
        return hab_cls(numero)

    def _crear_elemento(self, spec: dict, laberintos: dict, puertas_compartidas: dict):
        """
        Fábrica interna: devuelve el ElementoMapa correspondiente a 'spec'.

        Args:
            spec:               Diccionario con al menos la clave "tipo".
            laberintos:         Mapa id -> Laberinto ya creados.
            puertas_compartidas: Cache de puertas por id para reutilizarlas.

        Raises:
            ValueError: si el tipo es desconocido o falta información.
        """
        tipo = spec.get("tipo")
        if tipo == "pared":
            return Pared()

        if tipo == "puerta":
            pid = spec.get("id")
            if pid is None:
                return Puerta()
            if pid not in puertas_compartidas:
                puertas_compartidas[pid] = Puerta()
            return puertas_compartidas[pid]

        if tipo == "tunel":
            destino_id = spec.get("destino")
            if destino_id is None:
                raise ValueError("Un 'tunel' en el JSON debe indicar 'destino'")
            if destino_id not in laberintos:
                raise ValueError(f"Destino de tunel desconocido: '{destino_id}'")
            return Tunel(laberintos[destino_id])

        raise ValueError(f"Tipo de elemento desconocido en el JSON: '{tipo}'")
