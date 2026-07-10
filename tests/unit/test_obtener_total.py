from use_cases.agregar_gasto import AgregarGasto
from use_cases.obtener_total import ObtenerTotal
from infrastructure.repositorio_memoria import RepositorioMemoria

def test_total_sin_gastos():
    repo = RepositorioMemoria()
    assert ObtenerTotal(repo).ejecutar() == 0

def test_total_con_gastos():
    repo = RepositorioMemoria()
    AgregarGasto(repo).ejecutar("Almuerzo", 15.0, "alimentacion")
    AgregarGasto(repo).ejecutar("Bus", 2.50, "transporte")
    assert ObtenerTotal(repo).ejecutar() == 17.50
