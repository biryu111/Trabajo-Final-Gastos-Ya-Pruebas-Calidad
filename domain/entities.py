from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime
from typing import Optional

CATEGORIAS_PERMITIDAS = {
    "alimentacion", "transporte", "salud",
    "entretenimiento", "educacion", "otro"
}
ROLES_PERMITIDOS = {"admin", "casual"}

@dataclass
class Usuario:
    nombre: str
    correo: str
    password: str
    rol: str = "casual"
    activo: bool = True
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacio.")
        if not self.correo or "@" not in self.correo:
            raise ValueError("El correo no es valido.")
        if len(self.password) < 6:
            raise ValueError("La contrasena debe tener al menos 6 caracteres.")
        if self.rol not in ROLES_PERMITIDOS:
            raise ValueError(f"Rol invalido. Permitidos: {ROLES_PERMITIDOS}")

@dataclass
class Gasto:
    usuario_id: str
    descripcion: str
    monto: float
    categoria: str
    eliminado: bool = False
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None

    def __post_init__(self):
        if self.monto <= 0:
            raise ValueError("El monto debe ser mayor a cero.")
        if not self.descripcion or not self.descripcion.strip():
            raise ValueError("La descripcion no puede estar vacia.")
        if self.categoria not in CATEGORIAS_PERMITIDAS:
            raise ValueError(f"Categoria invalida. Permitidas: {CATEGORIAS_PERMITIDAS}")

@dataclass
class Presupuesto:
    usuario_id: str
    monto: float
    mes: int
    anio: int
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        if self.monto <= 0:
            raise ValueError("El presupuesto debe ser mayor a cero.")
