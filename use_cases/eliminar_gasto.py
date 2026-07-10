from domain.repositories import GastoRepository

class EliminarGasto:

    def __init__(self, repo: GastoRepository):
        self.repo = repo

    def ejecutar(self, id: str) -> bool:
        return self.repo.eliminar(id)
