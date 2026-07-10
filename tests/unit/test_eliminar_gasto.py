from use_cases.agregar_gasto import AgregarGasto
from use_cases.eliminar_gasto import EliminarGasto
from infrastructure.repositorio_memoria import RepositorioMemoria

def test_eliminar_gasto_existente():
    repo = RepositorioMemoria()
    gasto = AgregarGasto(repo).ejecutar("Taxi", 10.0, "transporte")
    resultado = EliminarGasto(repo).ejecutar(gasto.id)
    assert resultado is True

def test_eliminar_gasto_inexistente():
    repo = RepositorioMemoria()
    resultado = EliminarGasto(repo).ejecutar("id-que-no-existe")
    assert resultado is False
