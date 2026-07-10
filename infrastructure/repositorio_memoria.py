from typing import List
from domain.entities import Gasto
from domain.repositories import GastoRepository

class RepositorioMemoria(GastoRepository):

    def __init__(self):
        self._gastos: List[Gasto] = []

    def agregar(self, gasto: Gasto) -> Gasto:
        self._gastos.append(gasto)
        return gasto

    def listar(self) -> List[Gasto]:
        return list(self._gastos)

    def eliminar(self, id: str) -> bool:
        for i, g in enumerate(self._gastos):
            if g.id == id:
                self._gastos.pop(i)
                return True
        return False

    def obtener_total(self) -> float:
        return sum(g.monto for g in self._gastos)
