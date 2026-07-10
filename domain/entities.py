from dataclasses import dataclass, field
from uuid import uuid4

CATEGORIAS_PERMITIDAS = {"alimentacion", "transporte", "salud", "entretenimiento", "otro"}

@dataclass
class Gasto:
    descripcion: str
    monto: float
    categoria: str
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        if self.monto <= 0:
            raise ValueError("El monto debe ser mayor a cero.")
        if not self.descripcion or not self.descripcion.strip():
            raise ValueError("La descripcion no puede estar vacia.")
        if self.categoria not in CATEGORIAS_PERMITIDAS:
            raise ValueError(f"Categoria invalida. Permitidas: {CATEGORIAS_PERMITIDAS}")
