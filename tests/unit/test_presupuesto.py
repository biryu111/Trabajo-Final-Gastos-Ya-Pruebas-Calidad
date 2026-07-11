import pytest
from domain.entities import Presupuesto

def test_presupuesto_valido():
    p = Presupuesto(usuario_id="user-1", monto=1000.0, mes=7, anio=2026)
    assert p.monto == 1000.0

def test_presupuesto_monto_negativo():
    with pytest.raises(ValueError):
        Presupuesto(usuario_id="user-1", monto=-100, mes=7, anio=2026)

def test_presupuesto_monto_cero():
    with pytest.raises(ValueError):
        Presupuesto(usuario_id="user-1", monto=0, mes=7, anio=2026)
