from domain.entities import Gasto
from domain.repositories import GastoRepository

class AgregarGasto:

    def __init__(self, repo: GastoRepository):
        self.repo = repo

    def ejecutar(self, usuario_id: str, descripcion: str, monto: float, categoria: str) -> Gasto:
        gasto = Gasto(
            usuario_id=usuario_id,
            descripcion=descripcion,
            monto=monto,
            categoria=categoria
        )
        return self.repo.agregar(gasto)
