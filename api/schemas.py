from pydantic import BaseModel, field_validator
from domain.entities import CATEGORIAS_PERMITIDAS

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
    descripcion: str
    monto: float
    categoria: str

class TotalResponse(BaseModel):
    total: float
