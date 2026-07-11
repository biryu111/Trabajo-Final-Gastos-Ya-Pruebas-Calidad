import pytest
from domain.entities import Gasto

def test_gasto_valido():
    g = Gasto(usuario_id="user-1", descripcion="Almuerzo", monto=15.0, categoria="alimentacion")
    assert g.monto == 15.0
    assert g.eliminado == False

def test_gasto_monto_negativo():
    with pytest.raises(ValueError):
        Gasto(usuario_id="user-1", descripcion="Test", monto=-5, categoria="otro")

def test_gasto_monto_cero():
    with pytest.raises(ValueError):
        Gasto(usuario_id="user-1", descripcion="Test", monto=0, categoria="otro")

def test_gasto_descripcion_vacia():
    with pytest.raises(ValueError):
        Gasto(usuario_id="user-1", descripcion="", monto=10, categoria="otro")

def test_gasto_categoria_invalida():
    with pytest.raises(ValueError):
        Gasto(usuario_id="user-1", descripcion="Test", monto=10, categoria="invalida")
