from typing import List
from domain.entities import Gasto
from domain.repositories import GastoRepository
from infrastructure.database import SessionLocal
from infrastructure.models import GastoDb
from sqlalchemy import func

class RepositorioDb(GastoRepository):

    def agregar(self, gasto: Gasto) -> Gasto:
        db_gasto = GastoDb(
            id=gasto.id,
            descripcion=gasto.descripcion,
            monto=gasto.monto,
            categoria=gasto.categoria
        )
        with SessionLocal() as session:
            session.add(db_gasto)
            session.commit()
        return gasto

    def listar(self) -> List[Gasto]:
        with SessionLocal() as session:
            db_gastos = session.query(GastoDb).all()
            return [
                Gasto(
                    id=g.id,
                    descripcion=g.descripcion,
                    monto=g.monto,
                    categoria=g.categoria
                )
                for g in db_gastos
            ]

    def eliminar(self, id: str) -> bool:
        with SessionLocal() as session:
            db_gasto = session.query(GastoDb).filter(GastoDb.id == id).first()
            if db_gasto:
                session.delete(db_gasto)
                session.commit()
                return True
            return False

    def obtener_total(self) -> float:
        with SessionLocal() as session:
            total = session.query(func.sum(GastoDb.monto)).scalar()
            return float(total) if total is not None else 0.0
