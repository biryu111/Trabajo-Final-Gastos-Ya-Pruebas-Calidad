from use_cases.agregar_gasto import AgregarGasto
from use_cases.listar_gastos import ListarGastos
from infrastructure.repositorio_memoria import RepositorioMemoria

def test_listar_gastos_vacio():
    repo = RepositorioMemoria()
    caso_uso = ListarGastos(repo)
    assert caso_uso.ejecutar() == []

def test_listar_gastos_con_datos():
    repo = RepositorioMemoria()
    AgregarGasto(repo).ejecutar("Bus", 2.50, "transporte")
    AgregarGasto(repo).ejecutar("Medicina", 30.0, "salud")
    gastos = ListarGastos(repo).ejecutar()
    assert len(gastos) == 2
