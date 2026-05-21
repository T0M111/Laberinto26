"""
Tests del patrón Command aplicado a Puerta / ElementoMapa.

Roles probados:
  - Comando (Command)       : interfaz abstracta ejecutar()
  - Abrir (ConcreteCommand) : ejecutar() abre la puerta
  - Cerrar (ConcreteCommand): ejecutar() cierra la puerta
  - ElementoMapa (Invoker)  : lista +comandos (0..*)
  - Puerta (Receptor)       : receptor con abrir()/cerrar()

Propiedades verificadas:
  - Comando abstracto no se puede instanciar
  - Abrir.ejecutar() delega en receptor.abrir()
  - Cerrar.ejecutar() delega en receptor.cerrar()
  - Puerta.comandos contiene Abrir y Cerrar al crearse
  - ejecutar() a través de la lista de comandos cambia estado de la puerta
  - ElementoMapa base tiene atributo comandos (lista vacía)
  - Los comandos conocen su receptor
"""
import os
import sys
import unittest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(__file__))

from comando import Comando
from abrir import Abrir
from cerrar import Cerrar
from puerta import Puerta
from elemento_mapa import ElementoMapa


# ---------------------------------------------------------------------------
# Tests de Comando (interfaz abstracta)
# ---------------------------------------------------------------------------
class TestComandoAbstracto(unittest.TestCase):

    def test_no_se_puede_instanciar_directamente(self):
        receptor = MagicMock()
        with self.assertRaises(TypeError):
            Comando(receptor)

    def test_subclase_sin_ejecutar_no_instanciable(self):
        class CmdMalo(Comando):
            pass
        with self.assertRaises(TypeError):
            CmdMalo(MagicMock())

    def test_subclase_con_ejecutar_es_instanciable(self):
        class CmdBueno(Comando):
            def ejecutar(self):
                pass
        receptor = MagicMock()
        cmd = CmdBueno(receptor)
        self.assertIsInstance(cmd, Comando)
        self.assertIs(cmd.receptor, receptor)


# ---------------------------------------------------------------------------
# Tests de Abrir (ConcreteCommand)
# ---------------------------------------------------------------------------
class TestAbrir(unittest.TestCase):

    def test_es_instancia_de_Comando(self):
        puerta = Puerta()
        self.assertIsInstance(Abrir(puerta), Comando)

    def test_ejecutar_abre_la_puerta(self):
        puerta = Puerta()
        self.assertFalse(puerta.abierta)
        Abrir(puerta).ejecutar()
        self.assertTrue(puerta.abierta)

    def test_ejecutar_llama_abrir_del_receptor(self):
        receptor = MagicMock()
        Abrir(receptor).ejecutar()
        receptor.abrir.assert_called_once()

    def test_receptor_es_el_correcto(self):
        puerta = Puerta()
        cmd = Abrir(puerta)
        self.assertIs(cmd.receptor, puerta)

    def test_doble_ejecutar_deja_abierta(self):
        puerta = Puerta()
        cmd = Abrir(puerta)
        cmd.ejecutar()
        cmd.ejecutar()
        self.assertTrue(puerta.abierta)


# ---------------------------------------------------------------------------
# Tests de Cerrar (ConcreteCommand)
# ---------------------------------------------------------------------------
class TestCerrar(unittest.TestCase):

    def test_es_instancia_de_Comando(self):
        puerta = Puerta()
        self.assertIsInstance(Cerrar(puerta), Comando)

    def test_ejecutar_cierra_la_puerta(self):
        puerta = Puerta()
        puerta.abrir()  # poner en abierta primero
        self.assertTrue(puerta.abierta)
        Cerrar(puerta).ejecutar()
        self.assertFalse(puerta.abierta)

    def test_ejecutar_llama_cerrar_del_receptor(self):
        receptor = MagicMock()
        Cerrar(receptor).ejecutar()
        receptor.cerrar.assert_called_once()

    def test_receptor_es_el_correcto(self):
        puerta = Puerta()
        cmd = Cerrar(puerta)
        self.assertIs(cmd.receptor, puerta)

    def test_cerrar_puerta_ya_cerrada_sigue_cerrada(self):
        puerta = Puerta()
        self.assertFalse(puerta.abierta)
        Cerrar(puerta).ejecutar()
        self.assertFalse(puerta.abierta)


# ---------------------------------------------------------------------------
# Tests de ElementoMapa con +comandos
# ---------------------------------------------------------------------------
class TestElementoMapaComandos(unittest.TestCase):

    def test_elemento_mapa_tiene_atributo_comandos(self):
        puerta = Puerta()
        self.assertTrue(hasattr(puerta, "comandos"))

    def test_elemento_mapa_base_comandos_vacio(self):
        """Pared y otras hojas no específicas heredan la lista vacía de ElementoMapa."""
        from pared import Pared
        pared = Pared()
        self.assertEqual(pared.comandos, [])


# ---------------------------------------------------------------------------
# Tests de Puerta como Receptor e Invoker
# ---------------------------------------------------------------------------
class TestPuertaConComandos(unittest.TestCase):

    def setUp(self):
        self.puerta = Puerta()

    def test_puerta_tiene_dos_comandos(self):
        self.assertEqual(len(self.puerta.comandos), 2)

    def test_primer_comando_es_Abrir(self):
        self.assertIsInstance(self.puerta.comandos[0], Abrir)

    def test_segundo_comando_es_Cerrar(self):
        self.assertIsInstance(self.puerta.comandos[1], Cerrar)

    def test_comandos_tienen_puerta_como_receptor(self):
        for cmd in self.puerta.comandos:
            self.assertIs(cmd.receptor, self.puerta)

    def test_ejecutar_abrir_desde_lista_abre_puerta(self):
        self.assertFalse(self.puerta.abierta)
        self.puerta.comandos[0].ejecutar()
        self.assertTrue(self.puerta.abierta)

    def test_ejecutar_cerrar_desde_lista_cierra_puerta(self):
        self.puerta.abrir()
        self.puerta.comandos[1].ejecutar()
        self.assertFalse(self.puerta.abierta)

    def test_secuencia_abrir_cerrar_via_comandos(self):
        abrir_cmd, cerrar_cmd = self.puerta.comandos
        abrir_cmd.ejecutar()
        self.assertTrue(self.puerta.abierta)
        cerrar_cmd.ejecutar()
        self.assertFalse(self.puerta.abierta)

    def test_puertas_independientes_tienen_comandos_propios(self):
        otra = Puerta()
        self.puerta.comandos[0].ejecutar()
        self.assertTrue(self.puerta.abierta)
        self.assertFalse(otra.abierta)


if __name__ == "__main__":
    unittest.main()
