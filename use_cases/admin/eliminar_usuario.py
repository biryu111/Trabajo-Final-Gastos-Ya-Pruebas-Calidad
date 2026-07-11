from domain.repositories import UsuarioRepository

class EliminarUsuario:

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self, id: str) -> bool:
        usuario = self.repo.obtener_por_id(id)
        if not usuario:
            return False
        if usuario.rol == "admin":
            raise ValueError("No se puede eliminar un usuario administrador.")
        return self.repo.eliminar(id)
