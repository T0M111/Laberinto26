"""
Tests del patrón Observer aplicado a Juego / LaberintoGUI.

Roles probados:
  - Juego (Subject)          : suscribir(), desuscribir(), notificar()
  - Observador (Observer)    : interfaz abstracta actualizar()
  - LaberintoGUI (ConcreteObserver): back-ref +juego, actualizar() imprime estado

Propiedades verificadas:
  - Observador abstracto no se puede instanciar
  - suscribir enlaza el observador al sujeto
  - notificar() llama a actualizar() en cada observador suscrito
  - desuscribir quita el observador: ya no recibe notificaciones
  - doble suscripción no añade duplicados
  - notificar_ataque llama automáticamente a notificar()
  - LaberintoGUI.juego se actualiza con la referencia al Subject
  - Múltiples observadores reciben la misma notificación
"""
import os
import sys
import unittest
from unittest.mock import MagicMock, call, patch
from io import StringIO

sys.path.insert(0, os.path.dirname(__file__))

from observador import Observador
from laberinto_gui import LaberintoGUI
from juego import Juego
from bicho import Bicho
from personaje import Personaje
from modo import Agresivo, Perezoso


# ---------------------------------------------------------------------------
# Tests de Observador (interfaz abstracta)
# ---------------------------------------------------------------------------
class TestObservadorAbstracto(unittest.TestCase):

    def test_no_se_puede_instanciar_directamente(self):
        with self.assertRaises(TypeError):
            Observador()

    def test_subclase_sin_actualizar_no_instanciable(self):
        class ObsMalo(Observador):
            pass
        with self.assertRaises(TypeError):
            ObsMalo()

    def test_subclase_con_actualizar_es_instanciable(self):
        class ObsBueno(Observador):
            def actualizar(self, juego):
                pass
        obs = ObsBueno()
        self.assertIsInstance(obs, Observador)


# ---------------------------------------------------------------------------
# Tests de Juego como Subject
# ---------------------------------------------------------------------------
class TestJuegoSubject(unittest.TestCase):

    def _juego(self):
        return Juego()

    def _obs_mock(self):
        obs = MagicMock(spec=Observador)
        return obs

    def test_suscribir_agrega_observador(self):
        juego = self._juego()
        obs = self._obs_mock()
        juego.suscribir(obs)
        self.assertIn(obs, juego._observadores)

    def test_suscribir_duplicado_no_duplica(self):
        juego = self._juego()
        obs = self._obs_mock()
        juego.suscribir(obs)
        juego.suscribir(obs)
        self.assertEqual(juego._observadores.count(obs), 1)

    def test_desuscribir_elimina_observador(self):
        juego = self._juego()
        obs = self._obs_mock()
        juego.suscribir(obs)
        juego.desuscribir(obs)
        self.assertNotIn(obs, juego._observadores)

    def test_desuscribir_no_falla_si_no_suscrito(self):
        juego = self._juego()
        obs = self._obs_mock()
        juego.desuscribir(obs)  # no debe lanzar excepción

    def test_notificar_llama_actualizar_en_todos_los_observadores(self):
        juego = self._juego()
        obs1 = self._obs_mock()
        obs2 = self._obs_mock()
        juego.suscribir(obs1)
        juego.suscribir(obs2)
        juego.notificar()
        obs1.actualizar.assert_called_once_with(juego)
        obs2.actualizar.assert_called_once_with(juego)

    def test_notificar_sin_observadores_no_falla(self):
        juego = self._juego()
        juego.notificar()  # no debe lanzar excepción

    def test_observador_desuscrito_no_recibe_notificacion(self):
        juego = self._juego()
        obs = self._obs_mock()
        juego.suscribir(obs)
        juego.desuscribir(obs)
        juego.notificar()
        obs.actualizar.assert_not_called()

    def test_notificar_ataque_llama_notificar(self):
        """notificar_ataque() debe invocar notificar() automáticamente."""
        juego = self._juego()
        obs = self._obs_mock()
        juego.suscribir(obs)

        personaje = Personaje("Heroe", vidas=5, poder=2)
        bicho = Bicho("Goblin", Agresivo(), vidas=3, poder=1)
        juego.registrar_personaje(personaje)
        juego.registrar_bicho(bicho)

        juego.notificar_ataque(bicho, personaje)
        obs.actualizar.assert_called_once_with(juego)

    def test_multiples_ataques_multiple_notificaciones(self):
        juego = self._juego()
        obs = self._obs_mock()
        juego.suscribir(obs)

        personaje = Personaje("Heroe", vidas=10, poder=2)
        bicho = Bicho("Goblin", Agresivo(), vidas=10, poder=1)
        juego.registrar_personaje(personaje)
        juego.registrar_bicho(bicho)

        juego.notificar_ataque(bicho, personaje)
        juego.notificar_ataque(bicho, personaje)
        self.assertEqual(obs.actualizar.call_count, 2)

    def test_observadores_inicialmente_vacios(self):
        juego = self._juego()
        self.assertEqual(juego._observadores, [])


# ---------------------------------------------------------------------------
# Tests de LaberintoGUI (ConcreteObserver)
# ---------------------------------------------------------------------------
class TestLaberintoGUI(unittest.TestCase):

    def _setup(self):
        juego = Juego()
        personaje = Personaje("Heroe", vidas=5, poder=2)
        bicho = Bicho("Goblin", Agresivo(), vidas=3, poder=1)
        juego.registrar_personaje(personaje)
        juego.registrar_bicho(bicho)
        return juego, personaje, bicho

    def test_es_instancia_de_Observador(self):
        self.assertIsInstance(LaberintoGUI(), Observador)

    def test_juego_None_por_defecto(self):
        gui = LaberintoGUI()
        self.assertIsNone(gui.juego)

    def test_actualizar_asigna_referencia_juego(self):
        juego, _, _ = self._setup()
        gui = LaberintoGUI()
        gui.actualizar(juego)
        self.assertIs(gui.juego, juego)

    def test_actualizar_imprime_estado(self):
        juego, _, _ = self._setup()
        gui = LaberintoGUI()
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            gui.actualizar(juego)
            output = mock_out.getvalue()
        self.assertIn("LaberintoGUI", output)
        self.assertIn("Heroe", output)
        self.assertIn("Goblin", output)

    def test_actualizar_muestra_juego_en_curso(self):
        juego, _, _ = self._setup()
        gui = LaberintoGUI()
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            gui.actualizar(juego)
            output = mock_out.getvalue()
        self.assertIn("en curso", output)

    def test_actualizar_muestra_derrota(self):
        juego, personaje, _ = self._setup()
        gui = LaberintoGUI()
        personaje.recibir_danio(personaje.vidas)  # mata al personaje
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            gui.actualizar(juego)
            output = mock_out.getvalue()
        self.assertIn("Derrota", output)

    def test_actualizar_muestra_victoria(self):
        juego, _, bicho = self._setup()
        gui = LaberintoGUI()
        bicho.recibir_danio(bicho.vidas)  # mata al bicho
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            gui.actualizar(juego)
            output = mock_out.getvalue()
        self.assertIn("Victoria", output)

    def test_gui_recibe_notificacion_automatica_tras_ataque(self):
        """Tras suscribir la GUI, un ataque debe actualizar la GUI."""
        juego, personaje, bicho = self._setup()
        gui = LaberintoGUI()
        juego.suscribir(gui)
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            juego.notificar_ataque(bicho, personaje)
            output = mock_out.getvalue()
        self.assertIn("LaberintoGUI", output)


if __name__ == "__main__":
    unittest.main()
