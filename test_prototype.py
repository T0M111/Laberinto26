"""
Tests del patrón Prototype aplicado a Laberinto.

Roles probados:
  - Laberinto (Prototype)              : clone() devuelve copia profunda
  - LaberintoCuadrado (ConcreteProto A): clone() devuelve LaberintoCuadrado
  - LaberintoRombiforme (ConcreteProto B): clone() devuelve LaberintoRombiforme
  - Juego (Client)                     : clonarLaberinto() delega en laberinto.clone()

Propiedades verificadas:
  - El clon es una instancia del mismo tipo
  - El clon es un objeto distinto (no el mismo)
  - Los elementos (habitaciones) son copias, no referencias compartidas
  - Modificar el clon no afecta al original
  - LaberintoJsonBuilder crea el tipo correcto según "tipo" en el JSON
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from laberinto import Laberinto
from laberinto_cuadrado import LaberintoCuadrado
from laberinto_rombiforme import LaberintoRombiforme
from habitacion_cuadrada import HabitacionCuadrada
from habitacion_rombiforme import HabitacionRombiforme
from habitacion import Habitacion
from juego import Juego
from pared import Pared
from puerta import Puerta


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _lab_cuadrado_con_dos_habitaciones():
    lab = LaberintoCuadrado()
    lab.agregar_habitacion(HabitacionCuadrada(1))
    lab.agregar_habitacion(HabitacionCuadrada(2))
    return lab

def _lab_rombiforme_con_habitacion():
    lab = LaberintoRombiforme()
    lab.agregar_habitacion(HabitacionRombiforme(3))
    return lab


# ---------------------------------------------------------------------------
# Tests de Laberinto.clone() (Prototype base)
# ---------------------------------------------------------------------------
class TestLaberintoClone(unittest.TestCase):

    def test_clone_devuelve_instancia_distinta(self):
        lab = Laberinto()
        clon = lab.clone()
        self.assertIsNot(lab, clon)

    def test_clone_mismo_tipo(self):
        lab = Laberinto()
        clon = lab.clone()
        self.assertIsInstance(clon, Laberinto)

    def test_clone_copia_habitaciones(self):
        lab = Laberinto()
        lab.agregar_habitacion(Habitacion(1))
        clon = lab.clone()
        self.assertEqual(len(clon.habitaciones), 1)

    def test_clone_independiente_del_original(self):
        """Modificar el clon no altera el original."""
        lab = Laberinto()
        lab.agregar_habitacion(Habitacion(1))
        clon = lab.clone()
        clon.agregar_habitacion(Habitacion(2))
        self.assertEqual(len(lab.habitaciones), 1)
        self.assertEqual(len(clon.habitaciones), 2)

    def test_habitaciones_son_copias_distintas(self):
        lab = Laberinto()
        h = Habitacion(1)
        lab.agregar_habitacion(h)
        clon = lab.clone()
        self.assertIsNot(clon.obtener_habitacion(1), h)


# ---------------------------------------------------------------------------
# Tests de LaberintoCuadrado.clone() (ConcretePrototype A)
# ---------------------------------------------------------------------------
class TestLaberintoCuadradoClone(unittest.TestCase):

    def test_clone_devuelve_LaberintoCuadrado(self):
        lab = _lab_cuadrado_con_dos_habitaciones()
        clon = lab.clone()
        self.assertIsInstance(clon, LaberintoCuadrado)

    def test_clone_es_objeto_distinto(self):
        lab = _lab_cuadrado_con_dos_habitaciones()
        self.assertIsNot(lab, lab.clone())

    def test_clone_conserva_numero_de_habitaciones(self):
        lab = _lab_cuadrado_con_dos_habitaciones()
        self.assertEqual(len(lab.clone().habitaciones), 2)

    def test_clone_habitaciones_son_HabitacionCuadrada(self):
        lab = _lab_cuadrado_con_dos_habitaciones()
        for hab in lab.clone().habitaciones.values():
            self.assertIsInstance(hab, HabitacionCuadrada)

    def test_clone_independiente(self):
        lab = _lab_cuadrado_con_dos_habitaciones()
        clon = lab.clone()
        clon.agregar_habitacion(HabitacionCuadrada(99))
        self.assertEqual(len(lab.habitaciones), 2)


# ---------------------------------------------------------------------------
# Tests de LaberintoRombiforme.clone() (ConcretePrototype B)
# ---------------------------------------------------------------------------
class TestLaberintoRombiformeClone(unittest.TestCase):

    def test_clone_devuelve_LaberintoRombiforme(self):
        lab = _lab_rombiforme_con_habitacion()
        self.assertIsInstance(lab.clone(), LaberintoRombiforme)

    def test_clone_es_objeto_distinto(self):
        lab = _lab_rombiforme_con_habitacion()
        self.assertIsNot(lab, lab.clone())

    def test_clone_conserva_habitacion(self):
        lab = _lab_rombiforme_con_habitacion()
        self.assertEqual(len(lab.clone().habitaciones), 1)

    def test_clone_habitacion_es_HabitacionRombiforme(self):
        lab = _lab_rombiforme_con_habitacion()
        hab = list(lab.clone().habitaciones.values())[0]
        self.assertIsInstance(hab, HabitacionRombiforme)


# ---------------------------------------------------------------------------
# Tests de Juego.clonarLaberinto() (Client del Prototype)
# ---------------------------------------------------------------------------
class TestJuegoComoClientePrototype(unittest.TestCase):

    def test_clonarLaberinto_sin_laberinto_lanza_ValueError(self):
        juego = Juego()
        with self.assertRaises(ValueError):
            juego.clonarLaberinto()

    def test_clonarLaberinto_devuelve_copia(self):
        juego = Juego()
        juego.laberinto = _lab_cuadrado_con_dos_habitaciones()
        clon = juego.clonarLaberinto()
        self.assertIsNot(clon, juego.laberinto)

    def test_clonarLaberinto_mismo_tipo(self):
        juego = Juego()
        juego.laberinto = _lab_cuadrado_con_dos_habitaciones()
        self.assertIsInstance(juego.clonarLaberinto(), LaberintoCuadrado)

    def test_clonarLaberinto_rombiforme_mantiene_tipo(self):
        juego = Juego()
        juego.laberinto = _lab_rombiforme_con_habitacion()
        self.assertIsInstance(juego.clonarLaberinto(), LaberintoRombiforme)

    def test_clonarLaberinto_no_modifica_original(self):
        juego = Juego()
        juego.laberinto = _lab_cuadrado_con_dos_habitaciones()
        clon = juego.clonarLaberinto()
        clon.agregar_habitacion(HabitacionCuadrada(99))
        self.assertEqual(len(juego.laberinto.habitaciones), 2)


# ---------------------------------------------------------------------------
# Tests de integración: LaberintoJsonBuilder crea tipos correctos
# ---------------------------------------------------------------------------
class TestJsonBuilderCreaLaberintosTipados(unittest.TestCase):

    _CONFIG = os.path.join(os.path.dirname(__file__), "laberinto_config.json")

    def _construir(self):
        from laberinto_json_builder import LaberintoJsonBuilder
        from director import Director
        builder = LaberintoJsonBuilder(self._CONFIG)
        Director(builder).procesar()
        return builder.fabricarLaberinto()

    def test_laberinto_raiz_es_LaberintoCuadrado(self):
        lab = self._construir()
        self.assertIsInstance(lab, LaberintoCuadrado)

    def test_laberinto_raiz_tiene_dos_habitaciones(self):
        lab = self._construir()
        self.assertEqual(len(lab.habitaciones), 2)

    def test_clone_desde_json_mantiene_tipo(self):
        juego = Juego()
        juego.laberinto = self._construir()
        clon = juego.clonarLaberinto()
        self.assertIsInstance(clon, LaberintoCuadrado)

    def test_clone_desde_json_es_independiente(self):
        juego = Juego()
        juego.laberinto = self._construir()
        clon = juego.clonarLaberinto()
        clon.agregar_habitacion(HabitacionCuadrada(99))
        self.assertEqual(len(juego.laberinto.habitaciones), 2)


if __name__ == "__main__":
    unittest.main()
