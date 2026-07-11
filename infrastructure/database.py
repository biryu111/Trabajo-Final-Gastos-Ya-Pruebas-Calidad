import os
from urllib.parse import urlparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Mirleska777xd@localhost:5432/gastosya"
)

def create_database_if_not_exists(url: str):
    try:
        parsed = urlparse(url)
        db_name = parsed.path.lstrip('/')
        username = parsed.username
        password = parsed.password
        hostname = parsed.hostname or "localhost"
        port = parsed.port or 5432

        conn = psycopg2.connect(
            dbname="postgres",
            user=username,
            password=password,
            host=hostname,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar si la base de datos ya existe
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Base de datos '{db_name}' creada exitosamente.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al verificar/crear la base de datos: {e}")

# Aseguramos la existencia de la base de datos antes de inicializar SQLAlchemy
create_database_if_not_exists(DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
