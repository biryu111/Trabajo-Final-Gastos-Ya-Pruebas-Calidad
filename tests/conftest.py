import os
import pytest

# Configurar variable de entorno para la base de datos de pruebas antes de importar cualquier modulo
os.environ["DATABASE_URL"] = "postgresql://postgres:Mirleska777xd@localhost:5432/gastosya_test"

from infrastructure.database import engine, Base
from infrastructure.models import GastoDb
from sqlalchemy.orm import sessionmaker

SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Crear las tablas en la base de datos de prueba
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture(autouse=True)
def clean_db():
    # Limpiar la tabla de gastos antes de cada prueba para asegurar independencia
    with SessionLocalTest() as session:
        session.query(GastoDb).delete()
        session.commit()
