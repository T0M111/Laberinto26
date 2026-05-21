"""
Tests del patrón Visitor aplicado a la jerarquía de ElementoMapa.

Roles probados:
  - Visitador (Visitor)          : interfaz abstracta con visitarXxx()
  - VisitadorContador (ConcreteVisitor): cuenta Habitacion/Puerta/Pared
  - ElementoMapa                 : aceptar() abstracto
  - Habitacion (Element)         : aceptar() → visitarHabitacion + propaga hijos
  - Puerta (Element)             : aceptar() → visitarPuerta (doble despacho)
  - Pared (Element)              : aceptar() → visitarPared (doble despacho)
  - Armario (nuevo Contenedor)   : aceptar() propaga a hijos sin visita propia
  - Contenedor (base)            : aceptar() propaga hijos (hereda Laberinto/Tunel)

Propiedades verificadas:
  - Visitador abstracto no se puede instanciar
  - doble despacho: aceptar() en cada tipo llama al método visit correcto
  - VisitadorContador acumula conteos correctos
  - Habitacion.aceptar() visita la habitacion Y propaga a sus hijos
  - Armario.aceptar() solo propaga (no llama visitarArmario)
  - Laberinto.aceptar() propaga a todas sus habitaciones (hereda Contenedor)
  - Subclases concretas (ParedBomba, PuertaFuego, HabitacionCuadrada) usan
    el aceptar() heredado correctamente
"""
import os
import sys
import unittest
from unittest.mock import MagicMock, call

sys.path.insert(0, os.path.dirname(__file__))

from visitador import Visitador
from visitador_contador import VisitadorContador
from armario import Armario
from habitacion import Habitacion
from puerta import Puerta
from pared import Pared
from pared_bomba import ParedBomba
from puerta_fuego import PuertaFuego
from habitacion_cuadrada import HabitacionCuadrada
from laberinto import Laberinto
from orientacion import Norte, Sur, Este, Oeste


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _habitacion_simple(num=1):
    """Habitacion con Norte=Pared, Sur=Puerta, Este=Pared, Oeste=Pared."""
    h = Habitacion(num)
    h.establecer_lado(Norte(), Pared())
    h.establecer_lado(Sur(), Puerta())
    h.establecer_lado(Este(), Pared())
    h.establecer_lado(Oeste(), Pared())
    return h


def _visitador_mock():
    v = MagicMock(spec=Visitador)
    return v


# ---------------------------------------------------------------------------
# Tests de Visitador (interfaz abstracta)
# ---------------------------------------------------------------------------
class TestVisitadorAbstracto(unittest.TestCase):

    def test_no_se_puede_instanciar_directamente(self):
        with self.assertRaises(TypeError):
            Visitador()

    def test_subclase_incompleta_no_instanciable(self):
        class VMalo(Visitador):
            def visitarHabitacion(self, h): pass
            def visitarPuerta(self, p): pass
            # falta visitarPared
        with self.assertRaises(TypeError):
            VMalo()

    def test_subclase_completa_instanciable(self):
        class VBueno(Visitador):
            def visitarHabitacion(self, h): pass
            def visitarPuerta(self, p): pass
            def visitarPared(self, p): pass
        v = VBueno()
        self.assertIsInstance(v, Visitador)


# ---------------------------------------------------------------------------
# Tests de doble despacho: cada elemento llama al método correcto
# ---------------------------------------------------------------------------
class TestDobleDespacho(unittest.TestCase):

    def test_pared_llama_visitarPared(self):
        v = _visitador_mock()
        p = Pared()
        p.aceptar(v)
        v.visitarPared.assert_called_once_with(p)
        v.visitarPuerta.assert_not_called()
        v.visitarHabitacion.assert_not_called()

    def test_puerta_llama_visitarPuerta(self):
        v = _visitador_mock()
        p = Puerta()
        p.aceptar(v)
        v.visitarPuerta.assert_called_once_with(p)
        v.visitarPared.assert_not_called()
        v.visitarHabitacion.assert_not_called()

    def test_habitacion_llama_visitarHabitacion(self):
        v = _visitador_mock()
        h = Habitacion(1)
        h.aceptar(v)
        v.visitarHabitacion.assert_called_once_with(h)

    def test_pared_bomba_usa_visitarPared_heredado(self):
        v = _visitador_mock()
        pb = ParedBomba()
        pb.aceptar(v)
        v.visitarPared.assert_called_once_with(pb)

    def test_puerta_fuego_usa_visitarPuerta_heredado(self):
        v = _visitador_mock()
        pf = PuertaFuego()
        pf.aceptar(v)
        v.visitarPuerta.assert_called_once_with(pf)

    def test_habitacion_cuadrada_usa_visitarHabitacion_heredado(self):
        v = _visitador_mock()
        hc = HabitacionCuadrada(1)
        hc.aceptar(v)
        v.visitarHabitacion.assert_called_once_with(hc)


# ---------------------------------------------------------------------------
# Tests de propagación en Habitacion
# ---------------------------------------------------------------------------
class TestHabitacionAceptar(unittest.TestCase):

    def test_habitacion_propaga_a_hijos(self):
        v = _visitador_mock()
        h = _habitacion_simple(1)  # Norte=Pared, Sur=Puerta, Este=Pared, Oeste=Pared
        h.aceptar(v)
        # visitarHabitacion llamado una vez
        self.assertEqual(v.visitarHabitacion.call_count, 1)
        # visitarPared llamado 3 veces (N, E, O)
        self.assertEqual(v.visitarPared.call_count, 3)
        # visitarPuerta llamado 1 vez (S)
        self.assertEqual(v.visitarPuerta.call_count, 1)

    def test_habitacion_vacia_solo_visita_habitacion(self):
        v = _visitador_mock()
        h = Habitacion(2)
        h.aceptar(v)
        v.visitarHabitacion.assert_called_once_with(h)
        v.visitarPared.assert_not_called()
        v.visitarPuerta.assert_not_called()


# ---------------------------------------------------------------------------
# Tests de Armario
# ---------------------------------------------------------------------------
class TestArmarioAceptar(unittest.TestCase):

    def test_armario_vacio_no_llama_ningun_visit(self):
        v = _visitador_mock()
        a = Armario("TestArmario")
        a.aceptar(v)
        v.visitarHabitacion.assert_not_called()
        v.visitarPuerta.assert_not_called()
        v.visitarPared.assert_not_called()

    def test_armario_con_pared_llama_visitarPared(self):
        v = _visitador_mock()
        a = Armario()
        a.agregar_hijo(Pared())
        a.aceptar(v)
        v.visitarPared.assert_called_once()

    def test_armario_con_puerta_y_pared(self):
        v = _visitador_mock()
        a = Armario()
        a.agregar_hijo(Puerta())
        a.agregar_hijo(Pared())
        a.aceptar(v)
        self.assertEqual(v.visitarPuerta.call_count, 1)
        self.assertEqual(v.visitarPared.call_count, 1)

    def test_armario_no_llama_visitarArmario(self):
        """Armario.aceptar() NO llama a ningún método sobre sí mismo."""
        v = MagicMock()
        a = Armario()
        a.aceptar(v)
        # Solo puede haberse llamado si hubo hijos (no los hay)
        v.visitarArmario.assert_not_called()

    def test_armario_str(self):
        self.assertIn("Armario", str(Armario("X")))


# ---------------------------------------------------------------------------
# Tests de VisitadorContador (ConcreteVisitor)
# ---------------------------------------------------------------------------
class TestVisitadorContador(unittest.TestCase):

    def test_contadores_iniciales_a_cero(self):
        vc = VisitadorContador()
        self.assertEqual(vc.habitaciones, 0)
        self.assertEqual(vc.puertas, 0)
        self.assertEqual(vc.paredes, 0)

    def test_visitar_pared_incrementa_paredes(self):
        vc = VisitadorContador()
        vc.visitarPared(Pared())
        self.assertEqual(vc.paredes, 1)

    def test_visitar_puerta_incrementa_puertas(self):
        vc = VisitadorContador()
        vc.visitarPuerta(Puerta())
        self.assertEqual(vc.puertas, 1)

    def test_visitar_habitacion_incrementa_habitaciones(self):
        vc = VisitadorContador()
        vc.visitarHabitacion(Habitacion(1))
        self.assertEqual(vc.habitaciones, 1)

    def test_contador_habitacion_simple(self):
        """Habitacion con N/S/E/O: 1 habitacion, 3 paredes, 1 puerta."""
        vc = VisitadorContador()
        _habitacion_simple(1).aceptar(vc)
        self.assertEqual(vc.habitaciones, 1)
        self.assertEqual(vc.paredes, 3)
        self.assertEqual(vc.puertas, 1)

    def test_contador_laberinto_con_dos_habitaciones(self):
        """Laberinto con dos habitaciones simples: 2 hab, 6 paredes, 2 puertas."""
        lab = Laberinto()
        h1 = _habitacion_simple(1)
        h2 = _habitacion_simple(2)
        lab.agregar_habitacion(h1)
        lab.agregar_habitacion(h2)
        vc = VisitadorContador()
        lab.aceptar(vc)
        self.assertEqual(vc.habitaciones, 2)
        self.assertEqual(vc.paredes, 6)
        self.assertEqual(vc.puertas, 2)

    def test_es_instancia_de_Visitador(self):
        self.assertIsInstance(VisitadorContador(), Visitador)

    def test_str_muestra_contadores(self):
        vc = VisitadorContador()
        vc.visitarHabitacion(Habitacion(1))
        vc.visitarPared(Pared())
        s = str(vc)
        self.assertIn("habitaciones=1", s)
        self.assertIn("paredes=1", s)


# ---------------------------------------------------------------------------
# Tests de Contenedor base (Laberinto hereda aceptar)
# ---------------------------------------------------------------------------
class TestContenedorAceptarPropagacion(unittest.TestCase):

    def test_laberinto_propaga_a_habitaciones(self):
        v = _visitador_mock()
        lab = Laberinto()
        h1 = Habitacion(1)
        h2 = Habitacion(2)
        lab.agregar_habitacion(h1)
        lab.agregar_habitacion(h2)
        lab.aceptar(v)
        self.assertEqual(v.visitarHabitacion.call_count, 2)


if __name__ == "__main__":
    unittest.main()
