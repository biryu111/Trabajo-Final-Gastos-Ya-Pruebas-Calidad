from domain.repositories import GastoRepository

class ObtenerTotalesCategoria:

    def __init__(self, repo: GastoRepository):
        self.repo = repo

    def ejecutar(self, usuario_id: str) -> dict:
        return self.repo.obtener_totales_por_categoria(usuario_id)
