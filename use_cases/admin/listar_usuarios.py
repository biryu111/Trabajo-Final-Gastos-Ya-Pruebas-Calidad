from typing import List
from domain.entities import Usuario
from domain.repositories import UsuarioRepository

class ListarUsuarios:

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self) -> List[Usuario]:
        return self.repo.listar()
