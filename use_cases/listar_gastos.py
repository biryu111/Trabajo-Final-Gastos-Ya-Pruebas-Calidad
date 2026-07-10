from typing import List
from domain.entities import Gasto
from domain.repositories import GastoRepository

class ListarGastos:

    def __init__(self, repo: GastoRepository):
        self.repo = repo

    def ejecutar(self) -> List[Gasto]:
        return self.repo.listar()
