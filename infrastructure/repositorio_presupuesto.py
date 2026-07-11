from typing import Optional
from domain.entities import Presupuesto
from domain.repositories import PresupuestoRepository
from infrastructure.database import SessionLocal
from infrastructure.models import PresupuestoModel

class RepositorioPresupuesto(PresupuestoRepository):

    def obtener_por_usuario(self, usuario_id: str, mes: int, anio: int) -> Optional[Presupuesto]:
        with SessionLocal() as session:
            model = session.query(PresupuestoModel).filter(
                PresupuestoModel.usuario_id == usuario_id,
                PresupuestoModel.mes == mes,
                PresupuestoModel.anio == anio
            ).first()
            if model:
                return Presupuesto(
                    id=model.id,
                    usuario_id=model.usuario_id,
                    monto=model.monto,
                    mes=model.mes,
                    anio=model.anio
                )
            return None

    def guardar(self, presupuesto: Presupuesto) -> Presupuesto:
        with SessionLocal() as session:
            model = session.query(PresupuestoModel).filter(
                PresupuestoModel.usuario_id == presupuesto.usuario_id
            ).first()
            if model:
                model.monto = presupuesto.monto
                model.mes = presupuesto.mes
                model.anio = presupuesto.anio
            else:
                model = PresupuestoModel(
                    id=presupuesto.id,
                    usuario_id=presupuesto.usuario_id,
                    monto=presupuesto.monto,
                    mes=presupuesto.mes,
                    anio=presupuesto.anio
                )
                session.add(model)
            session.commit()
        return presupuesto
