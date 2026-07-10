from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import Gasto

class GastoRepository(ABC):

    @abstractmethod
    def agregar(self, gasto: Gasto) -> Gasto:
        pass

    @abstractmethod
    def listar(self) -> List[Gasto]:
        pass

    @abstractmethod
    def eliminar(self, id: str) -> bool:
        pass

    @abstractmethod
    def obtener_total(self) -> float:
        pass
