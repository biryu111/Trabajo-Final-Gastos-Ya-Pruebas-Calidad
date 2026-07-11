from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import Usuario, Gasto, Presupuesto

class UsuarioRepository(ABC):

    @abstractmethod
    def obtener_por_correo(self, correo: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def obtener_por_id(self, id: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def agregar(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    def listar(self) -> List[Usuario]:
        pass

    @abstractmethod
    def eliminar(self, id: str) -> bool:
        pass

class GastoRepository(ABC):

    @abstractmethod
    def agregar(self, gasto: Gasto) -> Gasto:
        pass

    @abstractmethod
    def listar(self, usuario_id: str) -> List[Gasto]:
        pass

    @abstractmethod
    def eliminar(self, id: str, usuario_id: Optional[str] = None) -> bool:
        pass

    @abstractmethod
    def obtener_total(self, usuario_id: str) -> float:
        pass

    @abstractmethod
    def listar_eliminados(self, usuario_id: str) -> List[Gasto]:
        pass

    @abstractmethod
    def obtener_por_id(self, id: str) -> Optional[Gasto]:
        pass

    @abstractmethod
    def obtener_totales_por_categoria(self, usuario_id: str) -> dict:
        pass

class PresupuestoRepository(ABC):

    @abstractmethod
    def obtener_por_usuario(self, usuario_id: str, mes: int, anio: int) -> Optional[Presupuesto]:
        pass

    @abstractmethod
    def guardar(self, presupuesto: Presupuesto) -> Presupuesto:
        pass
