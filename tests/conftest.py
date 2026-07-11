import os
import pytest

# Configurar variable de entorno para la base de datos de pruebas antes de importar cualquier modulo
os.environ["DATABASE_URL"] = "postgresql://postgres:Mirleska777xd@localhost:5432/gastosya_test"

from infrastructure.database import engine, Base
from infrastructure.models import UsuarioModel, GastoModel, PresupuestoModel
from sqlalchemy.orm import sessionmaker
import bcrypt
from uuid import uuid4

SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Crear las tablas
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture(autouse=True)
def clean_and_seed_db():
    # Limpiar todas las tablas
    with SessionLocalTest() as session:
        session.query(GastoModel).delete()
        session.query(PresupuestoModel).delete()
        session.query(UsuarioModel).delete()
        session.commit()
        
        # Insertar semillas para pruebas
        hashed_admin = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin = UsuarioModel(
            id=str(uuid4()),
            nombre="Biryu Admin",
            correo="biryu@admin.com",
            password=hashed_admin,
            rol="admin"
        )
        
        hashed_prueba = bcrypt.hashpw("prueba123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        prueba = UsuarioModel(
            id=str(uuid4()),
            nombre="Usuario Prueba",
            correo="prueba@gastosya.com",
            password=hashed_prueba,
            rol="casual"
        )
        
        session.add(admin)
        session.add(prueba)
        session.commit()
