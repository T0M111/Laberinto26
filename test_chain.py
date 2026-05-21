"""
Tests para el Patrón Chain of Responsibility — Laberinto26.

Estructura de participantes (del diagrama UML):
  - Handler (abstracto) : ElementoMapa — +sucesor, +cerrarPuertas()
  - ConcreteHandler que maneja : Puerta  — cerrarPuertas() cierra y continúa
  - ConcreteHandler que pasa   : Pared   — hereda comportamiento base (pasa al sucesor)
  - Client              : Juego  — +handler (1), lanza cerrarPuertas()

Cobertura:
  1.  ElementoMapa tiene +sucesor (None por defecto)
  2.  ElementoMapa.cerrarPuertas() pasa al sucesor si existe
  3.  ElementoMapa.cerrarPuertas() no falla si sucesor es None
  4.  Pared — hereda cerrarPuertas() de ElementoMapa (no override)
  5.  Puerta — cerrarPuertas() cierra la puerta
  6.  Puerta — cerrarPuertas() continúa la cadena al sucesor
  7.  Cadena mixta: Pared → Puerta → None
  8.  Cadena: Puerta → Puerta (ambas se cierran)
  9.  Cadena de sólo Paredes (nadie responde, no falla)
 10.  Juego — +handler (atributo, inicialmente None)
 11.  Juego.cerrarPuertas() sin handler lanza ValueError
 12.  Juego.cerrarPuertas() lanza la cadena desde el handler
 13.  Ciclo completo: handler con varias puertas y paredes
"""
import pytest

from elemento_mapa import ElementoMapa
from pared import Pared
from puerta import Puerta
from juego import Juego


# ===========================================================================
# 1–3. ElementoMapa — +sucesor y cerrarPuertas() base
# ===========================================================================

class TestElementoMapaSucesor:
    """ElementoMapa expone +sucesor inicialmente en None."""

    def test_sucesor_inicial_none(self):
        p = Pared()
        assert p.sucesor is None

    def test_sucesor_puerta_inicial_none(self):
        p = Puerta()
        assert p.sucesor is None

    def test_sucesor_asignable(self):
        p1 = Pared()
        p2 = Pared()
        p1.sucesor = p2
        assert p1.sucesor is p2

    def test_cerrar_puertas_sin_sucesor_no_falla(self):
        p = Pared()
        p.cerrarPuertas()   # no debe lanzar ninguna excepción

    def test_cerrar_puertas_pasa_al_sucesor(self):
        """Si ElementoMapa no sabe manejar la petición, la pasa al sucesor."""
        llamado = []

        class FakeHandler(Pared):
            def cerrarPuertas(self):
                llamado.append(True)

        pared = Pared()
        pared.sucesor = FakeHandler()
        pared.cerrarPuertas()
        assert llamado == [True]

    def test_cerrar_puertas_cadena_dos_paredes(self):
        """La petición recorre toda la cadena sin error."""
        p1 = Pared()
        p2 = Pared()
        p1.sucesor = p2
        p1.cerrarPuertas()   # no debe lanzar excepción


# ===========================================================================
# 4. Pared — hereda cerrarPuertas() sin override
# ===========================================================================

class TestParedCerrarPuertas:
    """Pared no sobrescribe cerrarPuertas(): simplemente pasa al sucesor."""

    def test_pared_no_tiene_cerrar_puertas_propio(self):
        # El método debe venir de ElementoMapa, no de Pared
        assert "cerrarPuertas" not in Pared.__dict__

    def test_pared_pasa_a_sucesor_puerta(self):
        pared = Pared()
        puerta = Puerta()
        puerta.abrir()       # la ponemos abierta para detectar el cambio
        pared.sucesor = puerta
        pared.cerrarPuertas()
        assert not puerta.abierta  # la puerta fue cerrada por la cadena


# ===========================================================================
# 5–6. Puerta — ConcreteHandler que maneja y continúa
# ===========================================================================

class TestPuertaCerrarPuertas:
    """Puerta sobrescribe cerrarPuertas(): se cierra y continúa la cadena."""

    def test_puerta_tiene_cerrar_puertas_propio(self):
        assert "cerrarPuertas" in Puerta.__dict__

    def test_cerrar_puertas_cierra_la_puerta(self):
        p = Puerta()
        p.abrir()
        assert p.abierta
        p.cerrarPuertas()
        assert not p.abierta

    def test_cerrar_puertas_sobre_puerta_ya_cerrada_no_falla(self):
        p = Puerta()
        assert not p.abierta
        p.cerrarPuertas()   # no lanza excepción
        assert not p.abierta

    def test_cerrar_puertas_continua_cadena(self):
        """Puerta cierra y también pasa al sucesor."""
        p1 = Puerta()
        p2 = Puerta()
        p1.abrir()
        p2.abrir()
        p1.sucesor = p2
        p1.cerrarPuertas()
        assert not p1.abierta
        assert not p2.abierta

    def test_cerrar_puertas_sin_sucesor_no_falla(self):
        p = Puerta()
        p.abrir()
        p.cerrarPuertas()   # sucesor es None, no debe fallar
        assert not p.abierta


# ===========================================================================
# 7–9. Cadenas mixtas
# ===========================================================================

class TestCadenasMixtas:
    """Cadenas de Paredes y Puertas entrelazadas."""

    def test_cadena_pared_puerta_none(self):
        """Pared → Puerta: la Puerta recibe la petición y se cierra."""
        pared = Pared()
        puerta = Puerta()
        puerta.abrir()
        pared.sucesor = puerta
        pared.cerrarPuertas()
        assert not puerta.abierta

    def test_cadena_puerta_pared_puerta(self):
        """Puerta → Pared → Puerta: ambas puertas se cierran."""
        p1 = Puerta()
        par = Pared()
        p2 = Puerta()
        p1.abrir()
        p2.abrir()
        p1.sucesor = par
        par.sucesor = p2
        p1.cerrarPuertas()
        assert not p1.abierta
        assert not p2.abierta

    def test_cadena_solo_paredes_no_falla(self):
        """Cadena de solo Paredes: nadie responde, no hay excepción."""
        p1, p2, p3 = Pared(), Pared(), Pared()
        p1.sucesor = p2
        p2.sucesor = p3
        p1.cerrarPuertas()   # OK

    def test_cadena_tres_puertas(self):
        """Tres Puertas encadenadas: todas se cierran."""
        a = Puerta()
        b = Puerta()
        c = Puerta()
        for p in (a, b, c):
            p.abrir()
        a.sucesor = b
        b.sucesor = c
        a.cerrarPuertas()
        assert not a.abierta
        assert not b.abierta
        assert not c.abierta

    def test_cadena_preserva_orden(self):
        """La cadena se ejecuta en orden: primero p1, luego p2."""
        orden = []

        class PuertaOrden(Puerta):
            def __init__(self, n):
                super().__init__()
                self.n = n
            def cerrarPuertas(self):
                orden.append(self.n)
                super().cerrarPuertas()

        p1 = PuertaOrden(1)
        p2 = PuertaOrden(2)
        p1.sucesor = p2
        p1.cerrarPuertas()
        assert orden == [1, 2]


# ===========================================================================
# 10–12. Juego — Client de Chain of Responsibility
# ===========================================================================

class TestJuegoClienteCoR:
    """Juego tiene +handler y lanza cerrarPuertas() en la cadena."""

    def test_handler_inicial_none(self):
        j = Juego()
        assert j.handler is None

    def test_handler_es_atributo_publico(self):
        j = Juego()
        assert hasattr(j, "handler")

    def test_cerrar_puertas_sin_handler_lanza_valueerror(self):
        j = Juego()
        with pytest.raises(ValueError):
            j.cerrarPuertas()

    def test_cerrar_puertas_lanza_cadena(self):
        """Juego.cerrarPuertas() delega en el primer handler."""
        j = Juego()
        puerta = Puerta()
        puerta.abrir()
        j.handler = puerta
        j.cerrarPuertas()
        assert not puerta.abierta

    def test_handler_puede_ser_pared(self):
        """El handler puede ser cualquier ElementoMapa."""
        j = Juego()
        j.handler = Pared()
        j.cerrarPuertas()   # no lanza excepción

    def test_cerrar_puertas_propaga_toda_la_cadena(self):
        j = Juego()
        p1 = Puerta()
        p2 = Puerta()
        p1.abrir()
        p2.abrir()
        p1.sucesor = p2
        j.handler = p1
        j.cerrarPuertas()
        assert not p1.abierta
        assert not p2.abierta


# ===========================================================================
# 13. Ciclo completo
# ===========================================================================

class TestCicloCompleto:
    """Ciclo realista: Juego con handler apuntando a una cadena mixta."""

    def test_ciclo_completo_con_paredes_y_puertas(self):
        """
        Cadena: Pared → Puerta → Pared → Puerta
        Solo las Puertas responden; las Paredes pasan.
        """
        j = Juego()
        pared1 = Pared()
        puerta1 = Puerta()
        pared2 = Pared()
        puerta2 = Puerta()
        puerta1.abrir()
        puerta2.abrir()

        # montar la cadena
        pared1.sucesor = puerta1
        puerta1.sucesor = pared2
        pared2.sucesor = puerta2
        j.handler = pared1

        j.cerrarPuertas()

        assert not puerta1.abierta
        assert not puerta2.abierta

    def test_ciclo_completo_estado_paredes_sin_cambio(self):
        """Las Paredes de la cadena no cambian de estado."""
        j = Juego()
        par = Pared()
        pue = Puerta()
        pue.abrir()
        par.sucesor = pue
        j.handler = par
        # no hay estado en Pared que verificar, pero no debe lanzar
        j.cerrarPuertas()
        assert not pue.abierta

    def test_reasignar_handler_cambia_cadena(self):
        """Cambiar j.handler redirige la cadena a un nuevo elemento."""
        j = Juego()
        puerta1 = Puerta()
        puerta2 = Puerta()
        puerta1.abrir()
        puerta2.abrir()

        j.handler = puerta1
        j.cerrarPuertas()
        assert not puerta1.abierta
        assert puerta2.abierta  # puerta2 NO estaba en la cadena

        puerta2_handler_nuevo = Puerta()
        puerta2_handler_nuevo.abrir()
        puerta2_handler_nuevo.sucesor = puerta2
        j.handler = puerta2_handler_nuevo
        j.cerrarPuertas()
        assert not puerta2.abierta
