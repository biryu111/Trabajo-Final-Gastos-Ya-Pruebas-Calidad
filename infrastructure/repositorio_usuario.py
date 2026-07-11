from typing import List, Optional
from domain.entities import Usuario
from domain.repositories import UsuarioRepository
from infrastructure.database import SessionLocal
from infrastructure.models import UsuarioModel

class RepositorioUsuario(UsuarioRepository):

    def obtener_por_correo(self, correo: str) -> Optional[Usuario]:
        with SessionLocal() as session:
            model = session.query(UsuarioModel).filter(UsuarioModel.correo == correo).first()
            if model:
                return Usuario(
                    id=model.id,
                    nombre=model.nombre,
                    correo=model.correo,
                    password=model.password,
                    rol=model.rol,
                    activo=model.activo,
                    created_at=model.created_at
                )
            return None

    def obtener_por_id(self, id: str) -> Optional[Usuario]:
        with SessionLocal() as session:
            model = session.query(UsuarioModel).filter(UsuarioModel.id == id).first()
            if model:
                return Usuario(
                    id=model.id,
                    nombre=model.nombre,
                    correo=model.correo,
                    password=model.password,
                    rol=model.rol,
                    activo=model.activo,
                    created_at=model.created_at
                )
            return None

    def agregar(self, usuario: Usuario) -> Usuario:
        model = UsuarioModel(
            id=usuario.id,
            nombre=usuario.nombre,
            correo=usuario.correo,
            password=usuario.password,
            rol=usuario.rol,
            activo=usuario.activo,
            created_at=usuario.created_at
        )
        with SessionLocal() as session:
            session.add(model)
            session.commit()
        return usuario

    def listar(self) -> List[Usuario]:
        with SessionLocal() as session:
            models = session.query(UsuarioModel).all()
            return [
                Usuario(
                    id=m.id,
                    nombre=m.nombre,
                    correo=m.correo,
                    password=m.password,
                    rol=m.rol,
                    activo=m.activo,
                    created_at=m.created_at
                )
                for m in models
            ]

    def eliminar(self, id: str) -> bool:
        with SessionLocal() as session:
            model = session.query(UsuarioModel).filter(UsuarioModel.id == id).first()
            if model:
                session.delete(model)
                session.commit()
                return True
            return False
