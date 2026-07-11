from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional, List
from datetime import datetime
from domain.entities import CATEGORIAS_PERMITIDAS, ROLES_PERMITIDOS

class LoginRequest(BaseModel):
    correo: str
    password: str

class LoginResponse(BaseModel):
    token: str

class RegistroRequest(BaseModel):
    nombre: str
    correo: str
    password: str

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacio.")
        return v

    @field_validator("correo")
    @classmethod
    def correo_valido(cls, v):
        if not v or "@" not in v:
            raise ValueError("El correo electronico no es valido.")
        return v

    @field_validator("password")
    @classmethod
    def password_valida(cls, v):
        if len(v) < 6:
            raise ValueError("La contrasena debe tener al menos 6 caracteres.")
        return v

class RegistroResponse(BaseModel):
    id: str
    nombre: str
    correo: str
    rol: str
    activo: bool

class UserMeResponse(BaseModel):
    id: str
    nombre: str
    correo: str
    rol: str

class GastoRequest(BaseModel):
    descripcion: str
    monto: float
    categoria: str

    @field_validator("monto")
    @classmethod
    def monto_positivo(cls, v):
        if v <= 0:
            raise ValueError("El monto debe ser mayor a cero.")
        return v

    @field_validator("descripcion")
    @classmethod
    def descripcion_no_vacia(cls, v):
        if not v or not v.strip():
            raise ValueError("La descripcion no puede estar vacia.")
        return v

    @field_validator("categoria")
    @classmethod
    def categoria_valida(cls, v):
        if v not in CATEGORIAS_PERMITIDAS:
            raise ValueError(f"Categoria invalida. Permitidas: {CATEGORIAS_PERMITIDAS}")
        return v

class GastoResponse(BaseModel):
    id: str
    usuario_id: str
    descripcion: str
    monto: float
    categoria: str
    eliminado: bool
    created_at: datetime
    deleted_at: Optional[datetime] = None

class TotalResponse(BaseModel):
    total: float

class CategoriaResumenItem(BaseModel):
    categoria: str
    total: float
    porcentaje: float

class PresupuestoRequest(BaseModel):
    monto: float
    mes: int
    anio: int

    @field_validator("monto")
    @classmethod
    def monto_positivo(cls, v):
        if v <= 0:
            raise ValueError("El presupuesto debe ser mayor a cero.")
        return v

    @field_validator("mes")
    @classmethod
    def mes_valido(cls, v):
        if v < 1 or v > 12:
            raise ValueError("El mes debe estar entre 1 y 12.")
        return v

    @field_validator("anio")
    @classmethod
    def anio_valido(cls, v):
        if v < 2000 or v > 2100:
            raise ValueError("El anio debe estar entre 2000 y 2100.")
        return v

class PresupuestoResponse(BaseModel):
    id: str
    usuario_id: str
    monto: float
    mes: int
    anio: int

class PresupuestoEstadoResponse(BaseModel):
    presupuesto: Optional[float]
    total_gastado: float
    saldo_restante: float
    superado: bool

class UserAdminResponse(BaseModel):
    id: str
    nombre: str
    correo: str
    password: str  # Hash visible
    rol: str
    activo: bool
    created_at: datetime
