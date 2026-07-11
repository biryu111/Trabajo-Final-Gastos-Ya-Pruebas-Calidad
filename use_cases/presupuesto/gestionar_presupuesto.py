from domain.entities import Presupuesto
from domain.repositories import PresupuestoRepository
from typing import Optional

class GestionarPresupuesto:

    def __init__(self, repo: PresupuestoRepository):
        self.repo = repo

    def obtener(self, usuario_id: str, mes: int, anio: int) -> Optional[Presupuesto]:
        return self.repo.obtener_por_usuario(usuario_id, mes, anio)

    def definir(self, usuario_id: str, monto: float, mes: int, anio: int) -> Presupuesto:
        presupuesto = Presupuesto(
            usuario_id=usuario_id,
            monto=monto,
            mes=mes,
            anio=anio
        )
        return self.repo.guardar(presupuesto)
