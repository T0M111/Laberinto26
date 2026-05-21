"""
Tests del patrón Proxy: Tunel.

Cobertura:
  - Tunel.__init__: raises ValueError si laberinto es None
  - Tunel.entrar: delega en la primera habitación del laberinto destino
  - Tunel.entrar: raises RuntimeError si el laberinto destino está vacío
  - Tunel.__str__: representación en string
  - LaberintoJsonBuilder: construye correctamente desde laberinto_config.json
  - LaberintoJsonBuilder: el laberinto raíz contiene un Tunel
  - LaberintoJsonBuilder: raises FileNotFoundError para ruta inexistente
"""
import os
import sys
import unittest

# Asegurar que se importa desde la carpeta del proyecto
sys.path.insert(0, os.path.dirname(__file__))

from laberinto import Laberinto
from habitacion import Habitacion
from pared import Pared
from tunel import Tunel
from director import Director
from laberinto_json_builder import LaberintoJsonBuilder
from orientacion import Norte, Sur, Este, Oeste
from bicho import Bicho
from modo import Perezoso


# ---------------------------------------------------------------------------
# Fixture mínimo de "alguien" para las llamadas a entrar()
# ---------------------------------------------------------------------------
class _Ente:
    """Stub mínimo con nombre y posicion para simular un Bicho en los tests."""
    def __init__(self, nombre="TestBicho"):
        self.nombre = nombre
        self.posicion = None

    def __str__(self):
        return self.nombre


# ---------------------------------------------------------------------------
# Tests de Tunel (patrón Proxy)
# ---------------------------------------------------------------------------
class TestTunel(unittest.TestCase):

    def _laberinto_con_hab(self, numero=10):
        """Crea un Laberinto mínimo con una habitación."""
        lab = Laberinto()
        hab = Habitacion(numero)
        hab.establecer_lado(Norte(), Pared())
        hab.establecer_lado(Sur(), Pared())
        hab.establecer_lado(Este(), Pared())
        hab.establecer_lado(Oeste(), Pared())
        lab.agregar_habitacion(hab)
        return lab, hab

    # --- Constructor ---

    def test_init_con_laberinto_valido(self):
        lab, _ = self._laberinto_con_hab()
        tunel = Tunel(lab)
        self.assertIs(tunel.laberinto, lab)

    def test_init_con_none_lanza_ValueError(self):
        with self.assertRaises(ValueError):
            Tunel(None)

    # --- entrar() ---

    def test_entrar_mueve_personaje_a_primera_habitacion(self):
        lab, primera_hab = self._laberinto_con_hab(numero=5)
        tunel = Tunel(lab)
        ente = _Ente()

        tunel.entrar(ente)

        self.assertIs(ente.posicion, primera_hab,
                      "El túnel debe teletransportar al ente a la primera habitación del laberinto")

    def test_entrar_laberinto_vacio_lanza_RuntimeError(self):
        lab_vacio = Laberinto()  # sin habitaciones
        tunel = Tunel(lab_vacio)
        ente = _Ente()
        with self.assertRaises(RuntimeError):
            tunel.entrar(ente)

    # --- __str__ ---

    def test_str_contiene_informacion_del_laberinto(self):
        lab, _ = self._laberinto_con_hab()
        tunel = Tunel(lab)
        texto = str(tunel)
        self.assertIn("Tunel", texto)
        self.assertIn(str(lab), texto)

    # --- Composite: Tunel hereda de Contenedor ---

    def test_tunel_es_instancia_de_contenedor(self):
        from contenedor import Contenedor
        lab, _ = self._laberinto_con_hab()
        tunel = Tunel(lab)
        self.assertIsInstance(tunel, Contenedor)


# ---------------------------------------------------------------------------
# Tests de LaberintoJsonBuilder (Builder + Proxy integrados)
# ---------------------------------------------------------------------------
class TestLaberintoJsonBuilder(unittest.TestCase):

    _CONFIG = os.path.join(os.path.dirname(__file__), "laberinto_config.json")

    def test_archivo_config_existe(self):
        self.assertTrue(os.path.isfile(self._CONFIG),
                        f"No existe laberinto_config.json en {os.path.dirname(__file__)}")

    def test_builder_devuelve_laberinto(self):
        builder = LaberintoJsonBuilder(self._CONFIG)
        director = Director(builder)
        lab = director.procesar()
        self.assertIsInstance(lab, Laberinto)

    def test_laberinto_raiz_tiene_dos_habitaciones(self):
        builder = LaberintoJsonBuilder(self._CONFIG)
        director = Director(builder)
        lab = director.procesar()
        self.assertEqual(len(lab.habitaciones), 2)

    def test_habitacion1_tiene_tunel_en_norte(self):
        builder = LaberintoJsonBuilder(self._CONFIG)
        director = Director(builder)
        lab = director.procesar()
        hab1 = lab.obtener_habitacion(1)
        lado_norte = hab1.obtener_lado(Norte())
        self.assertIsInstance(lado_norte, Tunel,
                              "El lado Norte de la habitación 1 debe ser un Tunel")

    def test_tunel_apunta_a_laberinto_secundario_con_habitacion3(self):
        builder = LaberintoJsonBuilder(self._CONFIG)
        director = Director(builder)
        lab = director.procesar()
        hab1 = lab.obtener_habitacion(1)
        tunel = hab1.obtener_lado(Norte())
        self.assertIn(3, tunel.laberinto.habitaciones,
                      "El laberinto destino debe contener la habitación 3")

    def test_tunel_teletransporta_a_habitacion3(self):
        builder = LaberintoJsonBuilder(self._CONFIG)
        director = Director(builder)
        lab = director.procesar()
        hab1 = lab.obtener_habitacion(1)
        tunel = hab1.obtener_lado(Norte())

        ente = _Ente()
        tunel.entrar(ente)

        hab3 = tunel.laberinto.obtener_habitacion(3)
        self.assertIs(ente.posicion, hab3)

    def test_builder_ruta_inexistente_lanza_FileNotFoundError(self):
        with self.assertRaises(FileNotFoundError):
            LaberintoJsonBuilder("ruta/que/no/existe.json")


if __name__ == "__main__":
    unittest.main()
