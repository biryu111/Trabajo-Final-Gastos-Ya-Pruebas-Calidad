import pytest
from use_cases.agregar_gasto import AgregarGasto
from infrastructure.repositorio_memoria import RepositorioMemoria

def test_agregar_gasto_valido():
    repo = RepositorioMemoria()
    caso_uso = AgregarGasto(repo)
    gasto = caso_uso.ejecutar("Almuerzo", 15.50, "alimentacion")
    assert gasto.descripcion == "Almuerzo"
    assert gasto.monto == 15.50
    assert gasto.categoria == "alimentacion"
    assert gasto.id is not None

def test_agregar_gasto_monto_invalido():
    repo = RepositorioMemoria()
    caso_uso = AgregarGasto(repo)
    with pytest.raises(ValueError):
        caso_uso.ejecutar("Almuerzo", -10, "alimentacion")

def test_agregar_gasto_descripcion_vacia():
    repo = RepositorioMemoria()
    caso_uso = AgregarGasto(repo)
    with pytest.raises(ValueError):
        caso_uso.ejecutar("", 10, "alimentacion")

def test_agregar_gasto_categoria_invalida():
    repo = RepositorioMemoria()
    caso_uso = AgregarGasto(repo)
    with pytest.raises(ValueError):
        caso_uso.ejecutar("Cine", 20, "diversión")
