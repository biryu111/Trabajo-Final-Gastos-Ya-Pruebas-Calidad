from typing import Optional
from domain.repositories import GastoRepository

class EliminarGasto:

    def __init__(self, repo: GastoRepository):
        self.repo = repo

    def ejecutar(self, id: str, usuario_id: Optional[str] = None) -> bool:
        gasto = self.repo.obtener_por_id(id)
        if not gasto:
            return False
        if usuario_id and gasto.usuario_id != usuario_id:
            return False
        return self.repo.eliminar(id, usuario_id)
