from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from infrastructure.database import Base

class UsuarioModel(Base):
    __tablename__ = "usuarios"
    id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    rol = Column(String, nullable=False, default="casual")
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class GastoModel(Base):
    __tablename__ = "gastos"
    id = Column(String, primary_key=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"), nullable=False)
    descripcion = Column(String, nullable=False)
    monto = Column(Float, nullable=False)
    categoria = Column(String, nullable=False)
    eliminado = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)

class PresupuestoModel(Base):
    __tablename__ = "presupuestos"
    id = Column(String, primary_key=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"), unique=True, nullable=False)
    monto = Column(Float, nullable=False)
    mes = Column(Integer, nullable=False)
    anio = Column(Integer, nullable=False)
