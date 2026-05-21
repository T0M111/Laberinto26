"""
Tests del patrón State aplicado al ciclo de vida de Ente.

Roles probados:
  - Estado (State abstracto)     : puedeActuar()
  - Vivo (ConcreteState A)       : puedeActuar() → True
  - Muerto (ConcreteState B)     : puedeActuar() → False
  - Ente (Context)               : actuar() delega en estado.puedeActuar()
  - Bicho (ConcreteContext)      : actuar() guarda con super().actuar()
  - Transición de estado         : Vivo → Muerto al llegar a 0 vidas

La prueba de que Ente.actuar() usa el State se verifica comprobando que:
  - Un ente vivo devuelve True  en actuar()
  - Un ente muerto devuelve False en actuar() sin ejecutar nada más
"""
import os
import sys
import unittest
from unittest.mock import MagicMock, call

sys.path.insert(0, os.path.dirname(__file__))

from estado_ente import Estado, Vivo, Muerto
from ente import Ente
from bicho import Bicho
from personaje import Personaje
from modo import Agresivo, Perezoso


# ---------------------------------------------------------------------------
# Tests de Estado (jerarquía)
# ---------------------------------------------------------------------------
class TestEstado(unittest.TestCase):

    def test_vivo_puedeActuar_true(self):
        self.assertTrue(Vivo().puedeActuar())

    def test_muerto_puedeActuar_false(self):
        self.assertFalse(Muerto().puedeActuar())

    def test_vivo_es_instancia_de_Estado(self):
        self.assertIsInstance(Vivo(), Estado)

    def test_muerto_es_instancia_de_Estado(self):
        self.assertIsInstance(Muerto(), Estado)

    def test_vivo_str(self):
        self.assertEqual(str(Vivo()), "Vivo")

    def test_muerto_str(self):
        self.assertEqual(str(Muerto()), "Muerto")

    def test_estado_es_abstracto(self):
        """Estado no se puede instanciar directamente."""
        with self.assertRaises(TypeError):
            Estado()


# ---------------------------------------------------------------------------
# Tests de Ente como Context del State
# ---------------------------------------------------------------------------
class TestEnteComoContextoState(unittest.TestCase):

    def _bicho(self, vidas=3):
        return Bicho("X", Perezoso(), vidas=vidas)

    def test_estado_inicial_es_Vivo(self):
        self.assertIsInstance(self._bicho().estado, Vivo)

    def test_actuar_devuelve_True_si_vivo(self):
        """Ente.actuar() delega en estado.puedeActuar() → True cuando Vivo."""
        b = self._bicho()
        self.assertTrue(b.actuar())

    def test_actuar_devuelve_False_si_muerto(self):
        """Ente.actuar() devuelve False cuando estado es Muerto."""
        b = self._bicho(vidas=1)
        b.recibir_danio(1)
        self.assertFalse(b.actuar())

    def test_transicion_a_Muerto_al_llegar_a_cero(self):
        b = self._bicho(vidas=2)
        b.recibir_danio(2)
        self.assertIsInstance(b.estado, Muerto)

    def test_no_transicion_antes_de_cero(self):
        b = self._bicho(vidas=3)
        b.recibir_danio(1)
        self.assertIsInstance(b.estado, Vivo)

    def test_esta_vivo_usa_estado_puedeActuar(self):
        """esta_vivo() es alias de estado.puedeActuar()."""
        b = self._bicho()
        self.assertEqual(b.esta_vivo(), b.estado.puedeActuar())

    def test_personaje_actuar_True_si_vivo(self):
        p = Personaje("Heroe")
        self.assertTrue(p.actuar())

    def test_personaje_actuar_False_si_muerto(self):
        p = Personaje("Heroe", vidas=1)
        p.recibir_danio(1)
        self.assertFalse(p.actuar())


# ---------------------------------------------------------------------------
# Tests de Bicho como ConcreteContext (guarda con super().actuar())
# ---------------------------------------------------------------------------
class TestBichoConStateguard(unittest.TestCase):

    def test_bicho_vivo_llama_modo_actua(self):
        """Bicho.actuar() llama a modo.actua(self) cuando está vivo."""
        modo_mock = MagicMock()
        b = Bicho("G", modo_mock, vidas=3)
        b.actuar()
        modo_mock.actua.assert_called_once_with(b)

    def test_bicho_muerto_no_llama_modo_actua(self):
        """Bicho.actuar() NO llama a modo.actua() cuando está muerto."""
        modo_mock = MagicMock()
        b = Bicho("G", modo_mock, vidas=1)
        b.recibir_danio(1)  # → estado Muerto
        b.actuar()
        modo_mock.actua.assert_not_called()

    def test_bicho_actua_varias_veces_mientras_vivo(self):
        modo_mock = MagicMock()
        b = Bicho("G", modo_mock, vidas=5)
        for _ in range(3):
            b.actuar()
        self.assertEqual(modo_mock.actua.call_count, 3)

    def test_bicho_no_actua_tras_morir(self):
        modo_mock = MagicMock()
        b = Bicho("G", modo_mock, vidas=2)
        b.actuar()           # vivo: actúa
        b.recibir_danio(2)   # muere
        b.actuar()           # muerto: no actúa
        modo_mock.actua.assert_called_once()  # solo 1 llamada (la primera)


if __name__ == "__main__":
    unittest.main()
