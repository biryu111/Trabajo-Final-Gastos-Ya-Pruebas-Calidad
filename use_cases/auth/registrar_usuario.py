import bcrypt
from domain.entities import Usuario
from domain.repositories import UsuarioRepository

class RegistrarUsuario:

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self, nombre: str, correo: str, password: str) -> Usuario:
        if self.repo.obtener_por_correo(correo):
            raise ValueError("El correo electronico ya esta registrado.")
        
        # Encriptar contraseña
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        usuario = Usuario(
            nombre=nombre,
            correo=correo,
            password=hashed,
            rol="casual"
        )
        return self.repo.agregar(usuario)
