"""
Tests para el Patrón Memento — Laberinto26.

Estructura de participantes:
  - Originator : Laberinto   (crearMemento, cargarPartida, estado)
  - Memento    : Memento     (getEstado, setEstado)
  - Caretaker  : Caretaker   (+memento)

Cobertura:
  1. Memento — creación y getEstado/setEstado
  2. Laberinto.estado — propiedad
  3. Laberinto.crearMemento() — genera un Memento con snapshot
  4. Snapshot es independiente (deepcopy)
  5. Laberinto.cargarPartida() — restaura habitaciones y _hijos
  6. Caretaker — atributo memento inicialmente None
  7. Caretaker.guardar() — crea y custodia Memento
  8. Caretaker.restaurar() — delega cargarPartida en el Laberinto
  9. Caretaker.restaurar() sin guardar — lanza ValueError
 10. Ciclo completo save/modify/restore
"""
import copy
import pytest

from laberinto import Laberinto
from habitacion import Habitacion
from memento import Memento
from caretaker import Caretaker


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def hacer_laberinto_con_habitaciones(*numeros):
    """Crea un Laberinto con las habitaciones numeradas en *numeros."""
    lab = Laberinto()
    for n in numeros:
        lab.agregar_habitacion(Habitacion(n))
    return lab


# ===========================================================================
# 1. Memento — creación y acceso al estado
# ===========================================================================

class TestMementoCreacion:
    """Memento se crea y devuelve el estado correctamente."""

    def test_memento_guarda_estado(self):
        datos = {"clave": 42}
        m = Memento(datos)
        assert m.getEstado() is datos

    def test_memento_estado_puede_ser_cualquier_objeto(self):
        m = Memento([1, 2, 3])
        assert m.getEstado() == [1, 2, 3]

    def test_memento_estado_none(self):
        m = Memento(None)
        assert m.getEstado() is None

    def test_memento_set_estado_actualiza(self):
        m = Memento("original")
        m.setEstado("nuevo")
        assert m.getEstado() == "nuevo"

    def test_memento_set_estado_reemplaza_completamente(self):
        m = Memento({"a": 1})
        nuevo = {"b": 2}
        m.setEstado(nuevo)
        assert m.getEstado() is nuevo

    def test_memento_multiples_sets(self):
        m = Memento(0)
        m.setEstado(1)
        m.setEstado(2)
        assert m.getEstado() == 2


# ===========================================================================
# 2. Laberinto.estado — propiedad
# ===========================================================================

class TestLaberintoEstado:
    """estado es una propiedad que expone las habitaciones actuales."""

    def test_estado_devuelve_habitaciones(self):
        lab = Laberinto()
        assert lab.estado is lab.habitaciones

    def test_estado_vacio_al_inicio(self):
        lab = Laberinto()
        assert lab.estado == {}

    def test_estado_refleja_habitaciones_agregadas(self):
        lab = hacer_laberinto_con_habitaciones(1, 2, 3)
        assert len(lab.estado) == 3

    def test_estado_actualiza_con_nueva_habitacion(self):
        lab = hacer_laberinto_con_habitaciones(1)
        lab.agregar_habitacion(Habitacion(2))
        assert 2 in lab.estado

    def test_estado_es_la_misma_referencia_que_habitaciones(self):
        lab = hacer_laberinto_con_habitaciones(1)
        # Son el mismo objeto
        assert lab.estado is lab.habitaciones


# ===========================================================================
# 3. Laberinto.crearMemento() — genera un Memento con snapshot
# ===========================================================================

class TestCrearMemento:
    """crearMemento devuelve un Memento con el estado actual del Laberinto."""

    def test_crea_memento_instancia_correcta(self):
        lab = Laberinto()
        m = lab.crearMemento()
        assert isinstance(m, Memento)

    def test_memento_contiene_habitaciones_actuales(self):
        lab = hacer_laberinto_con_habitaciones(1, 2)
        m = lab.crearMemento()
        assert set(m.getEstado().keys()) == {1, 2}

    def test_memento_laberinto_vacio(self):
        lab = Laberinto()
        m = lab.crearMemento()
        assert m.getEstado() == {}

    def test_memento_contiene_habitacion_correcta(self):
        lab = hacer_laberinto_con_habitaciones(7)
        m = lab.crearMemento()
        assert 7 in m.getEstado()

    def test_crear_varios_mementos_independientes(self):
        lab = hacer_laberinto_con_habitaciones(1)
        m1 = lab.crearMemento()
        lab.agregar_habitacion(Habitacion(2))
        m2 = lab.crearMemento()
        # m1 no debe reflejar la habitación 2
        assert 2 not in m1.getEstado()
        assert 2 in m2.getEstado()


# ===========================================================================
# 4. Snapshot es independiente (deepcopy)
# ===========================================================================

class TestSnapshotIndependiente:
    """El estado en el Memento es una copia profunda, independiente del Laberinto."""

    def test_modificar_laberinto_no_afecta_memento(self):
        lab = hacer_laberinto_con_habitaciones(1, 2)
        m = lab.crearMemento()
        lab.agregar_habitacion(Habitacion(3))
        assert 3 not in m.getEstado()

    def test_memento_no_es_la_misma_referencia_que_habitaciones(self):
        lab = hacer_laberinto_con_habitaciones(1)
        m = lab.crearMemento()
        assert m.getEstado() is not lab.habitaciones

    def test_memento_habitacion_no_es_la_misma_referencia(self):
        lab = hacer_laberinto_con_habitaciones(1)
        m = lab.crearMemento()
        # La habitación en el memento es una copia, no la original
        assert m.getEstado()[1] is not lab.habitaciones[1]

    def test_eliminar_habitacion_del_laberinto_no_afecta_memento(self):
        lab = hacer_laberinto_con_habitaciones(1, 2)
        m = lab.crearMemento()
        del lab.habitaciones[1]
        assert 1 in m.getEstado()

    def test_dos_mementos_son_independientes(self):
        lab = hacer_laberinto_con_habitaciones(1)
        m1 = lab.crearMemento()
        m2 = lab.crearMemento()
        assert m1.getEstado() is not m2.getEstado()


# ===========================================================================
# 5. Laberinto.cargarPartida() — restaura habitaciones y _hijos
# ===========================================================================

class TestCargarPartida:
    """cargarPartida restaura el estado del Laberinto desde un Memento."""

    def test_restaura_habitaciones(self):
        lab = hacer_laberinto_con_habitaciones(1, 2)
        m = lab.crearMemento()
        # modificar laberinto
        lab.agregar_habitacion(Habitacion(3))
        assert len(lab.habitaciones) == 3
        # restaurar
        lab.cargarPartida(m)
        assert len(lab.habitaciones) == 2

    def test_restaura_claves_correctas(self):
        lab = hacer_laberinto_con_habitaciones(10, 20)
        m = lab.crearMemento()
        lab.agregar_habitacion(Habitacion(30))
        lab.cargarPartida(m)
        assert set(lab.habitaciones.keys()) == {10, 20}

    def test_restaura_hijos_composite(self):
        lab = hacer_laberinto_con_habitaciones(1, 2)
        m = lab.crearMemento()
        lab.agregar_habitacion(Habitacion(3))
        lab.cargarPartida(m)
        assert len(lab._hijos) == 2

    def test_restaura_referencias_padre_en_hijos(self):
        lab = hacer_laberinto_con_habitaciones(1, 2)
        m = lab.crearMemento()
        lab.cargarPartida(m)
        for hab in lab._hijos:
            assert hab.padre is lab

    def test_cargar_laberinto_vacio_elimina_todo(self):
        lab_vacio = Laberinto()
        m = lab_vacio.crearMemento()
        lab = hacer_laberinto_con_habitaciones(1, 2, 3)
        lab.cargarPartida(m)
        assert lab.habitaciones == {}
        assert lab._hijos == []

    def test_str_refleja_estado_restaurado(self):
        lab = hacer_laberinto_con_habitaciones(1, 2)
        m = lab.crearMemento()
        lab.agregar_habitacion(Habitacion(3))
        lab.cargarPartida(m)
        assert "2" in str(lab)


# ===========================================================================
# 6. Caretaker — atributo memento
# ===========================================================================

class TestCaretakerAtributo:
    """Caretaker tiene un atributo +memento que comienza en None."""

    def test_memento_inicial_es_none(self):
        ct = Caretaker()
        assert ct.memento is None

    def test_memento_es_atributo_publico(self):
        ct = Caretaker()
        assert hasattr(ct, "memento")

    def test_memento_acepta_asignacion_directa(self):
        ct = Caretaker()
        m = Memento({})
        ct.memento = m
        assert ct.memento is m


# ===========================================================================
# 7. Caretaker.guardar() — crea y custodia Memento
# ===========================================================================

class TestCaretakerGuardar:
    """guardar() pide al Laberinto un Memento y lo almacena."""

    def test_guardar_crea_memento(self):
        lab = hacer_laberinto_con_habitaciones(1)
        ct = Caretaker()
        ct.guardar(lab)
        assert isinstance(ct.memento, Memento)

    def test_guardar_captura_estado_actual(self):
        lab = hacer_laberinto_con_habitaciones(1, 2)
        ct = Caretaker()
        ct.guardar(lab)
        assert set(ct.memento.getEstado().keys()) == {1, 2}

    def test_guardar_reemplaza_memento_anterior(self):
        lab = hacer_laberinto_con_habitaciones(1)
        ct = Caretaker()
        ct.guardar(lab)
        primer_memento = ct.memento
        lab.agregar_habitacion(Habitacion(2))
        ct.guardar(lab)
        assert ct.memento is not primer_memento

    def test_guardar_no_modifica_laberinto(self):
        lab = hacer_laberinto_con_habitaciones(1, 2)
        ct = Caretaker()
        ct.guardar(lab)
        assert len(lab.habitaciones) == 2


# ===========================================================================
# 8 & 9. Caretaker.restaurar()
# ===========================================================================

class TestCaretakerRestaurar:
    """restaurar() delega cargarPartida y lanza ValueError si no hay memento."""

    def test_restaurar_sin_memento_lanza_valueerror(self):
        ct = Caretaker()
        lab = Laberinto()
        with pytest.raises(ValueError):
            ct.restaurar(lab)

    def test_restaurar_llama_cargar_partida(self):
        lab = hacer_laberinto_con_habitaciones(1, 2)
        ct = Caretaker()
        ct.guardar(lab)
        lab.agregar_habitacion(Habitacion(3))
        ct.restaurar(lab)
        assert len(lab.habitaciones) == 2

    def test_restaurar_no_borra_memento_del_caretaker(self):
        lab = hacer_laberinto_con_habitaciones(1)
        ct = Caretaker()
        ct.guardar(lab)
        memento_guardado = ct.memento
        ct.restaurar(lab)
        assert ct.memento is memento_guardado


# ===========================================================================
# 10. Ciclo completo save / modify / restore
# ===========================================================================

class TestCicloCompleto:
    """Ciclo completo: guardar estado, modificar Laberinto, restaurar."""

    def test_ciclo_basico(self):
        lab = hacer_laberinto_con_habitaciones(1, 2)
        ct = Caretaker()
        ct.guardar(lab)

        lab.agregar_habitacion(Habitacion(3))
        assert len(lab.habitaciones) == 3

        ct.restaurar(lab)
        assert len(lab.habitaciones) == 2

    def test_restaurar_recupera_habitaciones_concretas(self):
        lab = hacer_laberinto_con_habitaciones(5, 6)
        ct = Caretaker()
        ct.guardar(lab)

        lab.agregar_habitacion(Habitacion(7))
        ct.restaurar(lab)

        assert 5 in lab.habitaciones
        assert 6 in lab.habitaciones
        assert 7 not in lab.habitaciones

    def test_restaurar_recupera_hijos_composite(self):
        lab = hacer_laberinto_con_habitaciones(1, 2)
        ct = Caretaker()
        ct.guardar(lab)
        lab.agregar_habitacion(Habitacion(3))
        ct.restaurar(lab)
        assert len(lab._hijos) == 2

    def test_doble_ciclo_guarda_el_ultimo(self):
        lab = hacer_laberinto_con_habitaciones(1)
        ct = Caretaker()

        ct.guardar(lab)                    # snapshot: {1}
        lab.agregar_habitacion(Habitacion(2))
        ct.guardar(lab)                    # snapshot: {1, 2}
        lab.agregar_habitacion(Habitacion(3))

        ct.restaurar(lab)
        assert set(lab.habitaciones.keys()) == {1, 2}

    def test_obtener_habitacion_tras_restaurar(self):
        lab = hacer_laberinto_con_habitaciones(1, 2)
        ct = Caretaker()
        ct.guardar(lab)
        lab.agregar_habitacion(Habitacion(3))
        ct.restaurar(lab)
        assert lab.obtener_habitacion(1) is not None
        assert lab.obtener_habitacion(2) is not None

    def test_str_laberinto_tras_restaurar(self):
        lab = hacer_laberinto_con_habitaciones(1, 2)
        ct = Caretaker()
        ct.guardar(lab)
        lab.agregar_habitacion(Habitacion(3))
        ct.restaurar(lab)
        assert "2" in str(lab)

    def test_estado_property_tras_restaurar(self):
        lab = hacer_laberinto_con_habitaciones(1, 2)
        ct = Caretaker()
        ct.guardar(lab)
        lab.agregar_habitacion(Habitacion(3))
        ct.restaurar(lab)
        assert lab.estado is lab.habitaciones
        assert len(lab.estado) == 2
