"""
Tests del patrón Mediator: Ente, Estado, Juego como mediador.

Cobertura:
  - Estado (State): Vivo.puedeActuar() y Muerto.puedeActuar()
  - Ente: vidas, poder, recibir_danio(), esta_vivo(), actuar(), transición Vivo->Muerto
  - Ente: ValueError en constructor para valores inválidos
  - Bicho(Ente): hereda vidas/poder/estado; mantiene nombre/modo/posicion
  - Personaje(Ente): hereda vidas/poder/estado; mantiene nombre/varita
  - Juego.registrar_personaje / registrar_bicho: enlace bidireccional
  - Juego.notificar_ataque: aplica daño y llama verificar_fin_juego
  - Juego.verificar_fin_juego: devuelve 'derrota' / 'victoria' / None
  - Juego.turno_bicho: ataca si en misma hab, actúa si no
  - Juego.turno_personaje: delega el ataque al mediador
  - LaberintoJsonBuilder.fabricar_entidades: crea personaje y bichos desde JSON
  - Regresión: tests de Proxy y Bridge siguen pasando (ejecutar juntos)
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from estado_ente import Estado, Vivo, Muerto
from ente import Ente
from bicho import Bicho
from personaje import Personaje
from modo import Agresivo, Perezoso
from juego import Juego
from habitacion import Habitacion
from orientacion import Norte, Sur, Este, Oeste
from pared import Pared


# ---------------------------------------------------------------------------
# Tests de Estado (State pattern) — renombrado de EstadoEnte
# ---------------------------------------------------------------------------
class TestEstadoEnte(unittest.TestCase):  # nombre mantenido por compatibilidad

    def test_vivo_puede_actuar(self):
        self.assertTrue(Vivo().puedeActuar())

    def test_muerto_no_puede_actuar(self):
        self.assertFalse(Muerto().puedeActuar())

    def test_vivo_str(self):
        self.assertEqual(str(Vivo()), "Vivo")

    def test_muerto_str(self):
        self.assertEqual(str(Muerto()), "Muerto")

    def test_vivo_es_instancia_de_Estado(self):
        self.assertIsInstance(Vivo(), Estado)

    def test_muerto_es_instancia_de_Estado(self):
        self.assertIsInstance(Muerto(), Estado)


# ---------------------------------------------------------------------------
# Tests de Ente (a través de Bicho, que es concreto)
# ---------------------------------------------------------------------------
class TestEnte(unittest.TestCase):

    def _bicho(self, vidas=3, poder=1):
        return Bicho("Test", Perezoso(), vidas=vidas, poder=poder)

    def test_estado_inicial_vivo(self):
        b = self._bicho()
        self.assertIsInstance(b.estado, Vivo)
        self.assertTrue(b.esta_vivo())
        self.assertTrue(b.actuar())  # State: actuar() delega en estado.puedeActuar()

    def test_recibir_danio_reduce_vidas(self):
        b = self._bicho(vidas=5)
        b.recibir_danio(2)
        self.assertEqual(b.vidas, 3)

    def test_recibir_danio_no_baja_de_cero(self):
        b = self._bicho(vidas=2)
        b.recibir_danio(10)
        self.assertEqual(b.vidas, 0)

    def test_recibir_danio_fatal_cambia_estado(self):
        b = self._bicho(vidas=1)
        b.recibir_danio(1)
        self.assertIsInstance(b.estado, Muerto)
        self.assertFalse(b.esta_vivo())
        self.assertFalse(b.actuar())  # State: muerto no puede actuar

    def test_vidas_invalidas_lanza_ValueError(self):
        with self.assertRaises(ValueError):
            Bicho("X", Perezoso(), vidas=0)

    def test_poder_invalido_lanza_ValueError(self):
        with self.assertRaises(ValueError):
            Bicho("X", Perezoso(), poder=0)

    def test_danio_invalido_lanza_ValueError(self):
        b = self._bicho()
        with self.assertRaises(ValueError):
            b.recibir_danio(0)

    def test_juego_inicialmente_none(self):
        self.assertIsNone(self._bicho()._juego)


# ---------------------------------------------------------------------------
# Tests de Bicho como Ente
# ---------------------------------------------------------------------------
class TestBichoComoEnte(unittest.TestCase):

    def test_bicho_es_instancia_de_ente(self):
        self.assertIsInstance(Bicho("G", Agresivo()), Ente)

    def test_bicho_constructor_compatibilidad(self):
        """El constructor de Bicho(nombre, modo) sigue funcionando sin vidas/poder."""
        b = Bicho("Goblin", Agresivo())
        self.assertEqual(b.vidas, 3)
        self.assertEqual(b.poder, 1)

    def test_bicho_con_vidas_y_poder_personalizados(self):
        b = Bicho("Troll", Perezoso(), vidas=10, poder=3)
        self.assertEqual(b.vidas, 10)
        self.assertEqual(b.poder, 3)


# ---------------------------------------------------------------------------
# Tests de Personaje como Ente
# ---------------------------------------------------------------------------
class TestPersonajeComoEnte(unittest.TestCase):

    def test_personaje_es_instancia_de_ente(self):
        self.assertIsInstance(Personaje("Heroe"), Ente)

    def test_personaje_sin_varita(self):
        p = Personaje("Heroe")
        self.assertIsNone(p.varita)
        self.assertEqual(p.vidas, 5)
        self.assertEqual(p.poder, 2)

    def test_personaje_con_varita_funciona(self):
        """Sigue siendo compatible con el patrón Adapter."""
        from bicho_adapter import BichoAdapter
        b = Bicho("Dragon", Agresivo())
        adapter = BichoAdapter(b)
        p = Personaje("Mago", varita=adapter)
        self.assertIsNotNone(p.varita)
        p.pedir_cambio_modo()  # no debe lanzar excepción


# ---------------------------------------------------------------------------
# Tests del Mediador (Juego)
# ---------------------------------------------------------------------------
class TestJuegoMediador(unittest.TestCase):

    def _setup(self, vidas_personaje=5, vidas_bicho=3):
        """Crea un Juego con un personaje y un bicho registrados."""
        juego = Juego()
        personaje = Personaje("Heroe", vidas=vidas_personaje, poder=2)
        bicho = Bicho("Goblin", Agresivo(), vidas=vidas_bicho, poder=1)
        juego.registrar_personaje(personaje)
        juego.registrar_bicho(bicho)
        return juego, personaje, bicho

    def test_registrar_personaje_enlace_bidireccional(self):
        juego, personaje, _ = self._setup()
        self.assertIs(juego.personaje, personaje)
        self.assertIs(personaje._juego, juego)

    def test_registrar_bicho_enlace_bidireccional(self):
        juego, _, bicho = self._setup()
        self.assertIn(bicho, juego.bichos)
        self.assertIs(bicho._juego, juego)

    def test_notificar_ataque_aplica_danio(self):
        juego, personaje, bicho = self._setup(vidas_personaje=5)
        juego.notificar_ataque(bicho, personaje)   # bicho.poder = 1
        self.assertEqual(personaje.vidas, 4)

    def test_verificar_fin_juego_none_si_juego_continua(self):
        juego, personaje, bicho = self._setup()
        self.assertIsNone(juego.verificar_fin_juego())

    def test_verificar_fin_juego_derrota_si_personaje_muerto(self):
        juego, personaje, bicho = self._setup(vidas_personaje=1)
        personaje.recibir_danio(1)
        self.assertEqual(juego.verificar_fin_juego(), "derrota")

    def test_verificar_fin_juego_victoria_si_todos_bichos_muertos(self):
        juego, _, bicho = self._setup(vidas_bicho=1)
        bicho.recibir_danio(1)
        self.assertEqual(juego.verificar_fin_juego(), "victoria")

    def test_notificar_ataque_devuelve_derrota(self):
        juego, personaje, bicho = self._setup(vidas_personaje=1)
        resultado = juego.notificar_ataque(bicho, personaje)
        self.assertEqual(resultado, "derrota")

    def test_notificar_ataque_devuelve_victoria(self):
        juego, personaje, bicho = self._setup(vidas_bicho=1)
        resultado = juego.notificar_ataque(personaje, bicho)
        self.assertEqual(resultado, "victoria")

    def test_turno_bicho_sin_personaje_en_misma_habitacion(self):
        """Si no están en la misma habitación, bicho actúa (no ataca)."""
        juego, personaje, bicho = self._setup()
        hab1 = Habitacion(1)
        hab2 = Habitacion(2)
        bicho.posicion = hab1
        personaje.posicion = hab2
        vidas_antes = personaje.vidas
        juego.turno_bicho(bicho)   # actúa (modo perezoso → duerme)
        self.assertEqual(personaje.vidas, vidas_antes)  # no hubo ataque

    def test_turno_bicho_en_misma_habitacion_ataca(self):
        """Si están en la misma habitación, el bicho ataca al personaje."""
        juego, personaje, bicho = self._setup(vidas_personaje=5)
        hab = Habitacion(1)
        bicho.posicion = hab
        personaje.posicion = hab
        juego.turno_bicho(bicho)
        self.assertEqual(personaje.vidas, 4)  # daño = bicho.poder = 1

    def test_turno_bicho_muerto_no_actua(self):
        juego, personaje, bicho = self._setup(vidas_bicho=1)
        bicho.recibir_danio(1)
        vidas_antes = personaje.vidas
        juego.turno_bicho(bicho)
        self.assertEqual(personaje.vidas, vidas_antes)

    def test_turno_personaje_ataca_bicho(self):
        juego, personaje, bicho = self._setup(vidas_bicho=5)
        resultado = juego.turno_personaje(bicho)  # personaje.poder = 2
        self.assertEqual(bicho.vidas, 3)

    def test_turno_personaje_sin_objetivo(self):
        juego, _, _ = self._setup()
        resultado = juego.turno_personaje()
        self.assertIsNone(resultado)


# ---------------------------------------------------------------------------
# Tests de integración: LaberintoJsonBuilder.fabricar_entidades
# ---------------------------------------------------------------------------
class TestFabricarEntidadesDesdeJson(unittest.TestCase):

    _CONFIG = os.path.join(os.path.dirname(__file__), "laberinto_config.json")

    def _construir(self):
        from laberinto_json_builder import LaberintoJsonBuilder
        from director import Director
        builder = LaberintoJsonBuilder(self._CONFIG)
        juego = Juego()
        director = Director(builder)
        director.procesar()
        builder.fabricar_entidades(juego)
        return juego

    def test_personaje_registrado(self):
        juego = self._construir()
        self.assertIsNotNone(juego.personaje)
        self.assertEqual(juego.personaje.nombre, "Heroe")

    def test_personaje_vidas_y_poder(self):
        juego = self._construir()
        self.assertEqual(juego.personaje.vidas, 5)
        self.assertEqual(juego.personaje.poder, 2)

    def test_dos_bichos_registrados(self):
        juego = self._construir()
        self.assertEqual(len(juego.bichos), 2)

    def test_goblin_agresivo(self):
        juego = self._construir()
        goblin = next(b for b in juego.bichos if b.nombre == "Goblin")
        self.assertIsInstance(goblin.modo, Agresivo)

    def test_troll_perezoso(self):
        juego = self._construir()
        troll = next(b for b in juego.bichos if b.nombre == "Troll")
        self.assertIsInstance(troll.modo, Perezoso)

    def test_personaje_tiene_referencia_al_juego(self):
        juego = self._construir()
        self.assertIs(juego.personaje._juego, juego)

    def test_bichos_tienen_referencia_al_juego(self):
        juego = self._construir()
        for b in juego.bichos:
            self.assertIs(b._juego, juego)


if __name__ == "__main__":
    unittest.main()
