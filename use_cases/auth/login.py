import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from domain.repositories import UsuarioRepository

SECRET_KEY = os.getenv("SECRET_KEY", "gastosya_secret_key_2024")
ALGORITHM = "HS256"

class Login:

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def ejecutar(self, correo: str, password: str) -> str:
        usuario = self.repo.obtener_por_correo(correo)
        if not usuario:
            raise ValueError("Credenciales incorrectas.")
        
        # Verificar contraseña
        if not bcrypt.checkpw(password.encode('utf-8'), usuario.password.encode('utf-8')):
            raise ValueError("Credenciales incorrectas.")
        
        # Generar Token JWT
        payload = {
            "sub": usuario.id,
            "correo": usuario.correo,
            "rol": usuario.rol,
            "nombre": usuario.nombre,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token
