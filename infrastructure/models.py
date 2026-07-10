from sqlalchemy import Column, String, Float
from infrastructure.database import Base

class GastoDb(Base):
    __tablename__ = "gastos"

    id = Column(String, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    monto = Column(Float, nullable=False)
    categoria = Column(String, nullable=False)
