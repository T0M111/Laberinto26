"""
Tests del patrón Flyweight aplicado a Moneda / FactoriaMonedas / Laberinto.

Roles probados:
  - Moneda (Flyweight)            : interfaz abstracta con value + posicion
  - Oro / Plata / SuperMoneda     : ConcreteFlyweight con value intrínseco fijo
  - FactoriaMonedas (Factory)     : pool +monedas; getMoneda(key) devuelve misma instancia
  - Laberinto (Client)            : tiene +factoria_monedas; usa getMoneda()

Propiedades verificadas:
  - Moneda abstracta no se puede instanciar
  - Oro/Plata/SuperMoneda tienen value correcto (10/5/50)
  - getMoneda devuelve la misma instancia para la misma clave (identidad)
  - getMoneda devuelve instancias distintas para claves distintas
  - Estado extrínseco (posicion) se puede cambiar sin afectar el value
  - Pool crece solo cuando se pide una clave nueva
  - Clave inválida lanza ValueError
  - Laberinto tiene factoria_monedas desde el inicio
  - monedas property devuelve flyweights del pool
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from moneda import Moneda
from oro import Oro
from plata import Plata
from super_moneda import SuperMoneda
from factoria_monedas import FactoriaMonedas
from laberinto import Laberinto
from habitacion import Habitacion


# ---------------------------------------------------------------------------
# Tests de Moneda (interfaz abstracta)
# ---------------------------------------------------------------------------
class TestMonedaAbstracta(unittest.TestCase):

    def test_no_se_puede_instanciar_directamente(self):
        with self.assertRaises(TypeError):
            Moneda()

    def test_subclase_sin_value_no_instanciable(self):
        class MonedaMala(Moneda):
            pass
        with self.assertRaises(TypeError):
            MonedaMala()

    def test_subclase_con_value_instanciable(self):
        class MonedaBuena(Moneda):
            @property
            def value(self):
                return 99
        m = MonedaBuena()
        self.assertIsInstance(m, Moneda)
        self.assertEqual(m.value, 99)

    def test_posicion_inicialmente_None(self):
        self.assertIsNone(Oro().posicion)


# ---------------------------------------------------------------------------
# Tests de ConcreteFlyweights
# ---------------------------------------------------------------------------
class TestConcreteFlyweights(unittest.TestCase):

    def test_oro_es_instancia_de_Moneda(self):
        self.assertIsInstance(Oro(), Moneda)

    def test_oro_value_es_10(self):
        self.assertEqual(Oro().value, 10)

    def test_plata_es_instancia_de_Moneda(self):
        self.assertIsInstance(Plata(), Moneda)

    def test_plata_value_es_5(self):
        self.assertEqual(Plata().value, 5)

    def test_super_moneda_es_instancia_de_Moneda(self):
        self.assertIsInstance(SuperMoneda(), Moneda)

    def test_super_moneda_value_es_50(self):
        self.assertEqual(SuperMoneda().value, 50)

    def test_posicion_extrinseca_se_puede_cambiar(self):
        h = Habitacion(1)
        m = Oro()
        m.posicion = h
        self.assertIs(m.posicion, h)

    def test_value_no_cambia_al_cambiar_posicion(self):
        m = Oro()
        m.posicion = Habitacion(1)
        self.assertEqual(m.value, 10)

    def test_str_incluye_tipo_y_value(self):
        s = str(Oro())
        self.assertIn("Oro", s)
        self.assertIn("10", s)


# ---------------------------------------------------------------------------
# Tests de FactoriaMonedas (Flyweight Factory)
# ---------------------------------------------------------------------------
class TestFactoriaMonedas(unittest.TestCase):

    def setUp(self):
        self.f = FactoriaMonedas()

    def test_get_oro_devuelve_instancia_Oro(self):
        self.assertIsInstance(self.f.getMoneda("oro"), Oro)

    def test_get_plata_devuelve_instancia_Plata(self):
        self.assertIsInstance(self.f.getMoneda("plata"), Plata)

    def test_get_super_moneda_devuelve_instancia_SuperMoneda(self):
        self.assertIsInstance(self.f.getMoneda("super_moneda"), SuperMoneda)

    def test_misma_clave_devuelve_misma_instancia(self):
        """Propiedad Flyweight: identidad garantizada por clave."""
        m1 = self.f.getMoneda("oro")
        m2 = self.f.getMoneda("oro")
        self.assertIs(m1, m2)

    def test_misma_clave_plata_misma_instancia(self):
        self.assertIs(self.f.getMoneda("plata"), self.f.getMoneda("plata"))

    def test_claves_distintas_instancias_distintas(self):
        oro = self.f.getMoneda("oro")
        plata = self.f.getMoneda("plata")
        self.assertIsNot(oro, plata)

    def test_pool_vacio_al_inicio(self):
        self.assertEqual(len(self.f), 0)

    def test_pool_crece_con_cada_nueva_clave(self):
        self.f.getMoneda("oro")
        self.assertEqual(len(self.f), 1)
        self.f.getMoneda("plata")
        self.assertEqual(len(self.f), 2)

    def test_pool_no_crece_con_clave_repetida(self):
        self.f.getMoneda("oro")
        self.f.getMoneda("oro")
        self.assertEqual(len(self.f), 1)

    def test_clave_invalida_lanza_ValueError(self):
        with self.assertRaises(ValueError):
            self.f.getMoneda("bronce")

    def test_monedas_property_devuelve_lista(self):
        self.f.getMoneda("oro")
        self.f.getMoneda("plata")
        monedas = self.f.monedas
        self.assertEqual(len(monedas), 2)
        tipos = {type(m) for m in monedas}
        self.assertIn(Oro, tipos)
        self.assertIn(Plata, tipos)

    def test_estado_extrinseco_compartido(self):
        """La posicion de un flyweight es compartida entre todas las referencias."""
        h1 = Habitacion(1)
        h2 = Habitacion(2)
        m1 = self.f.getMoneda("oro")
        m1.posicion = h1
        m2 = self.f.getMoneda("oro")  # misma instancia
        self.assertIs(m2.posicion, h1)
        m2.posicion = h2
        self.assertIs(m1.posicion, h2)  # ambas referencias ven el cambio


# ---------------------------------------------------------------------------
# Tests de Laberinto como cliente Flyweight
# ---------------------------------------------------------------------------
class TestLaberintoClienteFlyweight(unittest.TestCase):

    def test_laberinto_tiene_factoria_monedas(self):
        lab = Laberinto()
        self.assertIsInstance(lab.factoria_monedas, FactoriaMonedas)

    def test_laberinto_puede_obtener_moneda_oro(self):
        lab = Laberinto()
        m = lab.factoria_monedas.getMoneda("oro")
        self.assertIsInstance(m, Oro)
        self.assertEqual(m.value, 10)

    def test_laberinto_puede_asignar_posicion_a_moneda(self):
        lab = Laberinto()
        h = Habitacion(1)
        m = lab.factoria_monedas.getMoneda("plata")
        m.posicion = h
        self.assertIs(m.posicion, h)

    def test_dos_laberintos_tienen_factoria_independiente(self):
        lab1 = Laberinto()
        lab2 = Laberinto()
        self.assertIsNot(lab1.factoria_monedas, lab2.factoria_monedas)

    def test_laberinto_reutiliza_flyweight(self):
        lab = Laberinto()
        m1 = lab.factoria_monedas.getMoneda("super_moneda")
        m2 = lab.factoria_monedas.getMoneda("super_moneda")
        self.assertIs(m1, m2)


if __name__ == "__main__":
    unittest.main()
