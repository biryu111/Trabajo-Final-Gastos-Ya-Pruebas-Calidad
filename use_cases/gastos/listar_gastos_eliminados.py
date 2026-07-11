from typing import List
from domain.entities import Gasto
from domain.repositories import GastoRepository

class ListarGastosEliminados:

    def __init__(self, repo: GastoRepository):
        self.repo = repo

    def ejecutar(self, usuario_id: str) -> List[Gasto]:
        return self.repo.listar_eliminados(usuario_id)
