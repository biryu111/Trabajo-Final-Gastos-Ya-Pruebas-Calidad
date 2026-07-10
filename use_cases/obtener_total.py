from domain.repositories import GastoRepository

class ObtenerTotal:

    def __init__(self, repo: GastoRepository):
        self.repo = repo

    def ejecutar(self) -> float:
        return self.repo.obtener_total()
