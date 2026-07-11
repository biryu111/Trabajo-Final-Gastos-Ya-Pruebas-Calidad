from typing import Optional
from domain.entities import Usuario
from domain.repositories import UsuarioRepository

class ObtenerUsuario:

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self, user_id: str) -> Optional[Usuario]:
        return self.repo.obtener_por_id(user_id)
