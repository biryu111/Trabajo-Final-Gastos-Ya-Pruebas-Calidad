from domain.entities import Gasto
from domain.repositories import GastoRepository

class AgregarGasto:

    def __init__(self, repo: GastoRepository):
        self.repo = repo

    def ejecutar(self, descripcion: str, monto: float, categoria: str) -> Gasto:
        gasto = Gasto(descripcion=descripcion, monto=monto, categoria=categoria)
        return self.repo.agregar(gasto)
