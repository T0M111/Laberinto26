"""
Tests del patrón Bridge: Forma, HabitacionCuadrada, HabitacionRombiforme.

Cobertura:
  - Cuadrado: num=4, orientaciones cardinales
  - Rombo: num=4, orientaciones diagonales
  - HabitacionCuadrada: tiene forma Cuadrado, lados N/S/E/O inicializados con Pared
  - HabitacionCuadrada: acepta reemplazar lados
  - HabitacionRombiforme: tiene forma Rombo, lados NE/NO/SE/SO inicializados con Pared
  - Contenedor.forma: atributo presente (None por defecto en Contenedor base)
  - LaberintoJsonBuilder: construye HabitacionCuadrada y HabitacionRombiforme desde JSON
  - Los tests del Proxy siguen pasando (regresión)
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from forma import Cuadrado, Rombo
from habitacion import Habitacion
from habitacion_cuadrada import HabitacionCuadrada
from habitacion_rombiforme import HabitacionRombiforme
from contenedor import Contenedor
from pared import Pared
from puerta import Puerta
from orientacion import Norte, Sur, Este, Oeste, Noreste, Noroeste, Sureste, Suroeste
from laberinto import Laberinto
from laberinto_json_builder import LaberintoJsonBuilder
from director import Director


# ---------------------------------------------------------------------------
# Tests de Forma (Implementor)
# ---------------------------------------------------------------------------
class TestForma(unittest.TestCase):

    def test_cuadrado_num(self):
        self.assertEqual(Cuadrado().num, 4)

    def test_cuadrado_orientaciones_son_cardinales(self):
        nombres = {str(o) for o in Cuadrado().orientaciones}
        self.assertEqual(nombres, {"Norte", "Sur", "Este", "Oeste"})

    def test_rombo_num(self):
        self.assertEqual(Rombo().num, 4)

    def test_rombo_orientaciones_son_diagonales(self):
        nombres = {str(o) for o in Rombo().orientaciones}
        self.assertEqual(nombres, {"Noreste", "Noroeste", "Sureste", "Suroeste"})

    def test_forma_str_cuadrado(self):
        texto = str(Cuadrado())
        self.assertIn("Cuadrado", texto)
        self.assertIn("4", texto)

    def test_forma_str_rombo(self):
        texto = str(Rombo())
        self.assertIn("Rombo", texto)
        self.assertIn("4", texto)


# ---------------------------------------------------------------------------
# Tests de HabitacionCuadrada (Refined Abstraction A)
# ---------------------------------------------------------------------------
class TestHabitacionCuadrada(unittest.TestCase):

    def test_es_instancia_de_habitacion(self):
        self.assertIsInstance(HabitacionCuadrada(1), Habitacion)

    def test_forma_es_cuadrado(self):
        self.assertIsInstance(HabitacionCuadrada(1).forma, Cuadrado)

    def test_lados_cardinales_inicializados_con_pared(self):
        hab = HabitacionCuadrada(1)
        for ori in [Norte(), Sur(), Este(), Oeste()]:
            lado = hab.obtener_lado(ori)
            self.assertIsInstance(lado, Pared, f"El lado {ori} debería ser Pared")

    def test_no_tiene_lados_diagonales(self):
        hab = HabitacionCuadrada(1)
        for ori in [Noreste(), Noroeste(), Sureste(), Suroeste()]:
            self.assertIsNone(hab.obtener_lado(ori),
                              f"No debería tener lado {ori}")

    def test_establecer_lado_sobreescribe_pared(self):
        hab = HabitacionCuadrada(5)
        puerta = Puerta()
        hab.establecer_lado(Norte(), puerta)
        self.assertIs(hab.obtener_lado(Norte()), puerta)

    def test_str_incluye_numero(self):
        self.assertIn("7", str(HabitacionCuadrada(7)))

    def test_contenedor_forma_none_por_defecto(self):
        """El atributo +forma existe en Contenedor y vale None si no se asigna."""
        from laberinto import Laberinto
        lab = Laberinto()
        self.assertIsNone(lab.forma)


# ---------------------------------------------------------------------------
# Tests de HabitacionRombiforme (Refined Abstraction B)
# ---------------------------------------------------------------------------
class TestHabitacionRombiforme(unittest.TestCase):

    def test_es_instancia_de_habitacion(self):
        self.assertIsInstance(HabitacionRombiforme(2), Habitacion)

    def test_forma_es_rombo(self):
        self.assertIsInstance(HabitacionRombiforme(2).forma, Rombo)

    def test_lados_diagonales_inicializados_con_pared(self):
        hab = HabitacionRombiforme(2)
        for ori in [Noreste(), Noroeste(), Sureste(), Suroeste()]:
            lado = hab.obtener_lado(ori)
            self.assertIsInstance(lado, Pared, f"El lado {ori} debería ser Pared")

    def test_no_tiene_lados_cardinales(self):
        hab = HabitacionRombiforme(2)
        for ori in [Norte(), Sur(), Este(), Oeste()]:
            self.assertIsNone(hab.obtener_lado(ori),
                              f"No debería tener lado cardinal {ori}")

    def test_establecer_lado_sobreescribe_pared(self):
        hab = HabitacionRombiforme(8)
        puerta = Puerta()
        hab.establecer_lado(Noreste(), puerta)
        self.assertIs(hab.obtener_lado(Noreste()), puerta)

    def test_str_incluye_numero(self):
        self.assertIn("9", str(HabitacionRombiforme(9)))


# ---------------------------------------------------------------------------
# Tests de integración: LaberintoJsonBuilder con Bridge
# ---------------------------------------------------------------------------
class TestBridgeEnJson(unittest.TestCase):

    _CONFIG = os.path.join(os.path.dirname(__file__), "laberinto_config.json")

    def _construir(self):
        return Director(LaberintoJsonBuilder(self._CONFIG)).procesar()

    def test_habitacion1_es_cuadrada(self):
        lab = self._construir()
        hab1 = lab.obtener_habitacion(1)
        self.assertIsInstance(hab1, HabitacionCuadrada)

    def test_habitacion2_es_cuadrada(self):
        lab = self._construir()
        hab2 = lab.obtener_habitacion(2)
        self.assertIsInstance(hab2, HabitacionCuadrada)

    def test_habitacion3_es_rombiforme(self):
        from tunel import Tunel
        lab = self._construir()
        hab1 = lab.obtener_habitacion(1)
        tunel = hab1.obtener_lado(Norte())
        hab3 = tunel.laberinto.obtener_habitacion(3)
        self.assertIsInstance(hab3, HabitacionRombiforme)

    def test_habitacion3_tiene_lados_diagonales(self):
        from tunel import Tunel
        lab = self._construir()
        hab1 = lab.obtener_habitacion(1)
        tunel = hab1.obtener_lado(Norte())
        hab3 = tunel.laberinto.obtener_habitacion(3)
        for ori in [Noreste(), Noroeste(), Sureste(), Suroeste()]:
            self.assertIsNotNone(hab3.obtener_lado(ori),
                                 f"Habitacion 3 debe tener lado {ori}")

    def test_tipo_habitacion_desconocido_lanza_ValueError(self):
        import json, tempfile
        config = {
            "laberintos": [{"id": "x", "habitaciones": [
                {"numero": 1, "tipo": "habitacion_hexagonal",
                 "lados": {"norte": {"tipo": "pared"}}}
            ]}],
            "laberinto_raiz": "x"
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                         delete=False, encoding="utf-8") as f:
            json.dump(config, f)
            nombre = f.name
        try:
            with self.assertRaises(ValueError):
                Director(LaberintoJsonBuilder(nombre)).procesar()
        finally:
            os.unlink(nombre)


if __name__ == "__main__":
    unittest.main()
