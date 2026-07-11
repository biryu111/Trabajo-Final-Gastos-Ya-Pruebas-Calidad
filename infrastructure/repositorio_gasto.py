from typing import List, Optional
from datetime import datetime
from domain.entities import Gasto
from domain.repositories import GastoRepository
from infrastructure.database import SessionLocal
from infrastructure.models import GastoModel
from sqlalchemy import func

class RepositorioGasto(GastoRepository):

    def agregar(self, gasto: Gasto) -> Gasto:
        model = GastoModel(
            id=gasto.id,
            usuario_id=gasto.usuario_id,
            descripcion=gasto.descripcion,
            monto=gasto.monto,
            categoria=gasto.categoria,
            eliminado=gasto.eliminado,
            created_at=gasto.created_at,
            deleted_at=gasto.deleted_at
        )
        with SessionLocal() as session:
            session.add(model)
            session.commit()
        return gasto

    def listar(self, usuario_id: str) -> List[Gasto]:
        with SessionLocal() as session:
            models = session.query(GastoModel).filter(
                GastoModel.usuario_id == usuario_id,
                GastoModel.eliminado == False
            ).order_by(GastoModel.created_at.desc()).all()
            return [
                Gasto(
                    id=m.id,
                    usuario_id=m.usuario_id,
                    descripcion=m.descripcion,
                    monto=m.monto,
                    categoria=m.categoria,
                    eliminado=m.eliminado,
                    created_at=m.created_at,
                    deleted_at=m.deleted_at
                )
                for m in models
            ]

    def eliminar(self, id: str, usuario_id: Optional[str] = None) -> bool:
        with SessionLocal() as session:
            query = session.query(GastoModel).filter(GastoModel.id == id)
            if usuario_id:
                query = query.filter(GastoModel.usuario_id == usuario_id)
            model = query.first()
            if model and not model.eliminado:
                model.eliminado = True
                model.deleted_at = datetime.now()
                session.commit()
                return True
            return False

    def obtener_total(self, usuario_id: str) -> float:
        with SessionLocal() as session:
            total = session.query(func.sum(GastoModel.monto)).filter(
                GastoModel.usuario_id == usuario_id,
                GastoModel.eliminado == False
            ).scalar()
            return float(total) if total is not None else 0.0

    def listar_eliminados(self, usuario_id: str) -> List[Gasto]:
        with SessionLocal() as session:
            models = session.query(GastoModel).filter(
                GastoModel.usuario_id == usuario_id,
                GastoModel.eliminado == True
            ).order_by(GastoModel.deleted_at.desc()).all()
            return [
                Gasto(
                    id=m.id,
                    usuario_id=m.usuario_id,
                    descripcion=m.descripcion,
                    monto=m.monto,
                    categoria=m.categoria,
                    eliminado=m.eliminado,
                    created_at=m.created_at,
                    deleted_at=m.deleted_at
                )
                for m in models
            ]

    def obtener_por_id(self, id: str) -> Optional[Gasto]:
        with SessionLocal() as session:
            model = session.query(GastoModel).filter(GastoModel.id == id).first()
            if model:
                return Gasto(
                    id=model.id,
                    usuario_id=model.usuario_id,
                    descripcion=model.descripcion,
                    monto=model.monto,
                    categoria=model.categoria,
                    eliminado=model.eliminado,
                    created_at=model.created_at,
                    deleted_at=model.deleted_at
                )
            return None

    def obtener_totales_por_categoria(self, usuario_id: str) -> dict:
        with SessionLocal() as session:
            results = session.query(
                GastoModel.categoria,
                func.sum(GastoModel.monto)
            ).filter(
                GastoModel.usuario_id == usuario_id,
                GastoModel.eliminado == False
            ).group_by(GastoModel.categoria).all()
            return {cat: float(total) for cat, total in results}
