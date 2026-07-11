# GastosYa v2 — Gestor de Gastos con Autenticacion y Roles

## Descripcion del proyecto

Aplicacion web de gestion de gastos personales con sistema de autenticacion,
roles de usuario (administrador y casual), presupuesto mensual, historial de
gastos eliminados, categorias y dashboard personalizado por usuario.

Backend: Python + FastAPI + Clean Architecture
Base de datos: PostgreSQL con SQLAlchemy ORM
Frontend: HTML + CSS + JavaScript (una sola pagina por rol)
Autenticacion: JWT (JSON Web Tokens)

---

## Directives

```
gastosya/
├── main.py
├── requirements.txt
├── gastosya.md
├── index.html                    # Pagina de login/registro
├── admin.html                    # Dashboard administrador
├── usuario.html                  # Dashboard usuario casual
├── pytest.ini
├── .env.example
├── gastosya_backup.sql
│
├── domain/
│   ├── __init__.py
│   ├── entities.py               # Entidades: Usuario, Gasto, Categoria, Presupuesto
│   └── repositories.py          # Interfaces de repositorios
│
├── use_cases/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── login.py
│   │   ├── registrar_usuario.py
│   │   └── obtener_usuario.py
│   ├── gastos/
│   │   ├── __init__.py
│   │   ├── agregar_gasto.py
│   │   ├── listar_gastos.py
│   │   ├── eliminar_gasto.py
│   │   ├── obtener_total.py
│   │   └── listar_gastos_eliminados.py
│   ├── presupuesto/
│   │   ├── __init__.py
│   │   └── gestionar_presupuesto.py
│   └── admin/
│       ├── __init__.py
│       ├── listar_usuarios.py
│       ├── eliminar_usuario.py
│       └── ver_gastos_usuario.py
│
├── infrastructure/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── repositorio_usuario.py
│   ├── repositorio_gasto.py
│   └── repositorio_presupuesto.py
│
├── api/
│   ├── __init__.py
│   ├── schemas.py
│   ├── dependencies.py           # Verificacion JWT y roles
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── gastos.py
│       ├── presupuesto.py
│       └── admin.py
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── unit/
    │   ├── __init__.py
    │   ├── test_auth.py
    │   ├── test_gastos.py
    │   └── test_presupuesto.py
    ├── integration/
    │   ├── __init__.py
    │   └── test_api.py
    └── load/
        ├── __init__.py
        └── test_carga.py
```

---

## Analisis de Requisitos

### Historias de Usuario

#### HU-01 — Iniciar Sesion
**Como** usuario registrado
**quiero** iniciar sesion con mi correo y contrasena
**para** acceder a mi cuenta de forma segura.

**Criterios de aceptacion:**
- CA-01: El sistema valida correo y contrasena.
- CA-02: Si las credenciales son incorrectas, retorna error claro.
- CA-03: Al iniciar sesion, se genera un token JWT valido.
- CA-04: El token incluye el rol del usuario (admin o casual).

#### HU-02 — Registrar Usuario Casual
**Como** visitante
**quiero** crear una cuenta casual
**para** empezar a registrar mis gastos.

**Criterios de aceptacion:**
- CA-01: El correo debe ser unico en el sistema.
- CA-02: La contrasena debe tener al menos 6 caracteres.
- CA-03: El rol se asigna automaticamente como "casual".
- CA-04: No se puede registrar con rol "admin" desde el formulario publico.

#### HU-03 — Registrar Gasto
**Como** usuario autenticado
**quiero** registrar un gasto con descripcion, monto y categoria
**para** llevar control de mis finanzas.

**Criterios de aceptacion:**
- CA-01: El monto debe ser mayor a cero.
- CA-02: La descripcion no puede estar vacia.
- CA-03: La categoria debe ser valida.
- CA-04: El gasto se asocia automaticamente al usuario autenticado.
- CA-05: El gasto se registra en el historial.

#### HU-04 — Ver Mis Gastos
**Como** usuario autenticado
**quiero** ver solo mis gastos registrados
**para** revisar mis movimientos personales.

**Criterios de aceptacion:**
- CA-01: Solo se muestran los gastos del usuario autenticado.
- CA-02: Se puede filtrar por categoria.
- CA-03: Se muestra el total acumulado.

#### HU-05 — Eliminar Gasto
**Como** usuario autenticado
**quiero** eliminar un gasto
**para** corregir errores de registro.

**Criterios de aceptacion:**
- CA-01: Solo se puede eliminar gastos propios.
- CA-02: El gasto eliminado se mueve al historial de eliminados.
- CA-03: El gasto eliminado no aparece en la lista activa.

#### HU-06 — Gestionar Presupuesto Mensual
**Como** usuario autenticado
**quiero** definir un presupuesto mensual maximo
**para** saber cuanto dinero me queda disponible.

**Criterios de aceptacion:**
- CA-01: El presupuesto debe ser mayor a cero.
- CA-02: El sistema muestra cuanto se ha gastado vs el presupuesto.
- CA-03: Se muestra el saldo restante (presupuesto - total gastado).
- CA-04: Si se supera el presupuesto, se muestra una alerta visual.

#### HU-07 — Ver Categorias de Gastos
**Como** usuario autenticado
**quiero** ver un resumen de mis gastos por categoria
**para** identificar en que gasto mas.

**Criterios de aceptacion:**
- CA-01: Se muestra el total gastado por cada categoria.
- CA-02: Se muestra el porcentaje que representa cada categoria.

#### HU-08 — Panel de Administrador
**Como** administrador
**quiero** ver y gestionar todos los usuarios y sus gastos
**para** tener control total del sistema.

**Criterios de aceptacion:**
- CA-01: El admin puede listar todos los usuarios.
- CA-02: El admin puede ver los gastos de cualquier usuario.
- CA-03: El admin puede eliminar gastos de cualquier usuario.
- CA-04: El admin puede eliminar cuentas de usuarios casuales.
- CA-05: El admin puede ver el historial de gastos eliminados de cualquier usuario.
- CA-06: El admin puede ver las contraseñas de los usuarios (hash visible).
- CA-07: Solo el admin puede acceder al panel de administracion.

---

## Reglas de Negocio

| ID | Regla |
|----|-------|
| RN-01 | El monto de un gasto debe ser estrictamente mayor a cero. |
| RN-02 | La descripcion no puede estar vacia o contener solo espacios. |
| RN-03 | La categoria debe pertenecer al conjunto: alimentacion, transporte, salud, entretenimiento, educacion, otro. |
| RN-04 | Cada gasto tiene un ID unico UUID autogenerado. |
| RN-05 | No se puede eliminar un gasto inexistente. |
| RN-06 | Un usuario solo puede ver y gestionar sus propios gastos. |
| RN-07 | El administrador puede gestionar todos los gastos y usuarios. |
| RN-08 | No se puede registrar con rol admin desde el formulario publico. |
| RN-09 | El correo electronico debe ser unico en el sistema. |
| RN-10 | Los gastos eliminados se mueven al historial, no se borran fisicamente. |
| RN-11 | El presupuesto mensual es individual por usuario. |
| RN-12 | Solo puede existir un usuario admin en el sistema (biryu@admin.com). |

---

## Modelos de Base de Datos

### Tabla: usuarios
```sql
id          VARCHAR PRIMARY KEY  -- UUID
nombre      VARCHAR NOT NULL
correo      VARCHAR UNIQUE NOT NULL
password    VARCHAR NOT NULL     -- hash bcrypt
rol         VARCHAR NOT NULL     -- 'admin' o 'casual'
activo      BOOLEAN DEFAULT TRUE
created_at  TIMESTAMP
```

### Tabla: gastos
```sql
id            VARCHAR PRIMARY KEY  -- UUID
usuario_id    VARCHAR FK -> usuarios.id
descripcion   VARCHAR NOT NULL
monto         DOUBLE PRECISION NOT NULL
categoria     VARCHAR NOT NULL
eliminado     BOOLEAN DEFAULT FALSE
created_at    TIMESTAMP
deleted_at    TIMESTAMP NULL
```

### Tabla: presupuestos
```sql
id          VARCHAR PRIMARY KEY
usuario_id  VARCHAR FK -> usuarios.id UNIQUE
monto       DOUBLE PRECISION NOT NULL
mes         INTEGER
anio        INTEGER
```

---

## Arquitectura — Clean Architecture

```
[ API Layer ]      <-- FastAPI routers, schemas, JWT middleware
      |
[ Use Cases ]      <-- Logica de negocio por dominio (auth, gastos, admin)
      |
[ Domain ]         <-- Entidades, interfaces de repositorios
      |
[ Infrastructure ] <-- SQLAlchemy ORM, PostgreSQL, repositorios concretos
```

---

## Endpoints REST

### Autenticacion (publico)
| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| POST | /auth/login | Iniciar sesion, retorna JWT |
| POST | /auth/registro | Registrar nuevo usuario casual |
| GET | /auth/me | Obtener datos del usuario autenticado |

### Gastos (usuario autenticado)
| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| POST | /gastos/ | Registrar un nuevo gasto |
| GET | /gastos/ | Listar gastos activos del usuario |
| DELETE | /gastos/{id} | Mover gasto al historial de eliminados |
| GET | /gastos/total | Total acumulado del usuario |
| GET | /gastos/eliminados | Historial de gastos eliminados del usuario |
| GET | /gastos/categorias | Resumen de gastos por categoria |

### Presupuesto (usuario autenticado)
| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| POST | /presupuesto/ | Definir presupuesto mensual |
| GET | /presupuesto/ | Ver presupuesto y saldo restante |
| PUT | /presupuesto/ | Actualizar presupuesto |

### Administracion (solo admin)
| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /admin/usuarios | Listar todos los usuarios |
| DELETE | /admin/usuarios/{id} | Eliminar usuario casual |
| GET | /admin/usuarios/{id}/gastos | Ver gastos de un usuario |
| GET | /admin/usuarios/{id}/eliminados | Ver historial eliminados de usuario |
| DELETE | /admin/gastos/{id} | Eliminar gasto de cualquier usuario |

---

## Datos Iniciales (Seed)

Al iniciar la app por primera vez, crear automaticamente:

### Usuario Administrador:
```json
{
  "nombre": "Biryu Admin",
  "correo": "biryu@admin.com",
  "password": "admin123",
  "rol": "admin"
}
```

### Usuario Casual de prueba:
```json
{
  "nombre": "Usuario Prueba",
  "correo": "prueba@gastosya.com",
  "password": "prueba123",
  "rol": "casual"
}
```

---

## Implementacion

### domain/entities.py
```python
from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime
from typing import Optional

CATEGORIAS_PERMITIDAS = {
    "alimentacion", "transporte", "salud",
    "entretenimiento", "educacion", "otro"
}
ROLES_PERMITIDOS = {"admin", "casual"}

@dataclass
class Usuario:
    nombre: str
    correo: str
    password: str
    rol: str = "casual"
    activo: bool = True
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacio.")
        if not self.correo or "@" not in self.correo:
            raise ValueError("El correo no es valido.")
        if len(self.password) < 6:
            raise ValueError("La contrasena debe tener al menos 6 caracteres.")
        if self.rol not in ROLES_PERMITIDOS:
            raise ValueError(f"Rol invalido. Permitidos: {ROLES_PERMITIDOS}")

@dataclass
class Gasto:
    usuario_id: str
    descripcion: str
    monto: float
    categoria: str
    eliminado: bool = False
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None

    def __post_init__(self):
        if self.monto <= 0:
            raise ValueError("El monto debe ser mayor a cero.")
        if not self.descripcion or not self.descripcion.strip():
            raise ValueError("La descripcion no puede estar vacia.")
        if self.categoria not in CATEGORIAS_PERMITIDAS:
            raise ValueError(f"Categoria invalida. Permitidas: {CATEGORIAS_PERMITIDAS}")

@dataclass
class Presupuesto:
    usuario_id: str
    monto: float
    mes: int
    anio: int
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        if self.monto <= 0:
            raise ValueError("El presupuesto debe ser mayor a cero.")
```

### infrastructure/database.py
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:admin123@localhost:5432/gastosya"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### infrastructure/models.py
```python
from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from infrastructure.database import Base

class UsuarioModel(Base):
    __tablename__ = "usuarios"
    id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    rol = Column(String, nullable=False, default="casual")
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class GastoModel(Base):
    __tablename__ = "gastos"
    id = Column(String, primary_key=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"), nullable=False)
    descripcion = Column(String, nullable=False)
    monto = Column(Float, nullable=False)
    categoria = Column(String, nullable=False)
    eliminado = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)

class PresupuestoModel(Base):
    __tablename__ = "presupuestos"
    id = Column(String, primary_key=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"), unique=True, nullable=False)
    monto = Column(Float, nullable=False)
    mes = Column(Integer, nullable=False)
    anio = Column(Integer, nullable=False)
```

### api/dependencies.py
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "gastosya_secret_key_2024")
ALGORITHM = "HS256"
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalido.")

def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado. Se requiere rol admin.")
    return current_user
```

### main.py
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from infrastructure.database import engine, Base, SessionLocal
from infrastructure.models import UsuarioModel
from api.routers import auth, gastos, presupuesto, admin
import bcrypt
from uuid import uuid4

app = FastAPI(
    title="GastosYa v2",
    description="Gestor de gastos personales con roles y autenticacion",
    version="2.0.0"
)

app.include_router(auth.router)
app.include_router(gastos.router)
app.include_router(presupuesto.router)
app.include_router(admin.router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Crear admin si no existe
        admin_existente = db.query(UsuarioModel).filter(
            UsuarioModel.correo == "biryu@admin.com"
        ).first()
        if not admin_existente:
            hashed = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
            admin_user = UsuarioModel(
                id=str(uuid4()),
                nombre="Biryu Admin",
                correo="biryu@admin.com",
                password=hashed,
                rol="admin"
            )
            db.add(admin_user)
            db.commit()

        # Crear usuario de prueba si no existe
        prueba_existente = db.query(UsuarioModel).filter(
            UsuarioModel.correo == "prueba@gastosya.com"
        ).first()
        if not prueba_existente:
            hashed = bcrypt.hashpw("prueba123".encode(), bcrypt.gensalt()).decode()
            prueba_user = UsuarioModel(
                id=str(uuid4()),
                nombre="Usuario Prueba",
                correo="prueba@gastosya.com",
                password=hashed,
                rol="casual"
            )
            db.add(prueba_user)
            db.commit()
    finally:
        db.close()

@app.get("/")
def inicio():
    return FileResponse("index.html")

@app.get("/admin-panel")
def admin_panel():
    return FileResponse("admin.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("usuario.html")
```

---

## Interfaz de Usuario

### index.html — Pantalla de Login/Registro
Diseno moderno en modo oscuro con:
- Logo y nombre GastosYa centrado
- Formulario de login con correo y contrasena
- Boton para cambiar a formulario de registro
- Formulario de registro con nombre, correo y contrasena
- Al iniciar sesion: si rol=admin → redirigir a /admin-panel, si rol=casual → redirigir a /dashboard
- Validacion de campos en el frontend
- Mensajes de error claros

### usuario.html — Dashboard Usuario Casual
Diseno moderno en modo oscuro con navegacion lateral o pestanas:

**Pestana 1 — Resumen (inicio)**
- Total gastado del mes
- Presupuesto mensual configurado
- Saldo restante (con barra de progreso y alerta si se supera)
- Ultimos 5 gastos

**Pestana 2 — Mis Gastos**
- Tabla con todos los gastos activos
- Filtro por categoria
- Boton eliminar en cada gasto
- Boton agregar nuevo gasto (formulario modal)

**Pestana 3 — Categorias**
- Tarjetas o grafico por categoria
- Total gastado por categoria
- Porcentaje del total que representa

**Pestana 4 — Presupuesto**
- Formulario para definir/actualizar presupuesto mensual
- Barra de progreso visual
- Alerta visual si se supera el presupuesto (color rojo)

**Pestana 5 — Historial**
- Lista de gastos eliminados con fecha de eliminacion
- Solo lectura

**Header:**
- Nombre del usuario
- Boton cerrar sesion

### admin.html — Panel Administrador
Diseno moderno en modo oscuro con navegacion lateral:

**Pestana 1 — Dashboard General**
- Total de usuarios registrados
- Total de gastos en el sistema
- Usuarios mas activos

**Pestana 2 — Usuarios**
- Tabla con todos los usuarios (nombre, correo, rol, password hash, fecha registro)
- Boton eliminar usuario casual
- Boton ver gastos de ese usuario

**Pestana 3 — Gastos por Usuario**
- Selector de usuario
- Tabla con gastos activos del usuario seleccionado
- Boton eliminar gasto
- Total del usuario

**Pestana 4 — Historial de Eliminados**
- Selector de usuario
- Lista de gastos eliminados con fecha

**Header:**
- "Panel Administrador"
- Nombre del admin
- Boton cerrar sesion

---

## Pruebas

### tests/unit/test_auth.py
```python
import pytest
from domain.entities import Usuario

def test_crear_usuario_valido():
    u = Usuario(nombre="Ana", correo="ana@test.com", password="123456")
    assert u.nombre == "Ana"
    assert u.rol == "casual"

def test_usuario_nombre_vacio():
    with pytest.raises(ValueError):
        Usuario(nombre="", correo="ana@test.com", password="123456")

def test_usuario_correo_invalido():
    with pytest.raises(ValueError):
        Usuario(nombre="Ana", correo="correo_sin_arroba", password="123456")

def test_usuario_password_corta():
    with pytest.raises(ValueError):
        Usuario(nombre="Ana", correo="ana@test.com", password="123")

def test_usuario_rol_invalido():
    with pytest.raises(ValueError):
        Usuario(nombre="Ana", correo="ana@test.com", password="123456", rol="superadmin")
```

### tests/unit/test_gastos.py
```python
import pytest
from domain.entities import Gasto

def test_gasto_valido():
    g = Gasto(usuario_id="user-1", descripcion="Almuerzo", monto=15.0, categoria="alimentacion")
    assert g.monto == 15.0
    assert g.eliminado == False

def test_gasto_monto_negativo():
    with pytest.raises(ValueError):
        Gasto(usuario_id="user-1", descripcion="Test", monto=-5, categoria="otro")

def test_gasto_monto_cero():
    with pytest.raises(ValueError):
        Gasto(usuario_id="user-1", descripcion="Test", monto=0, categoria="otro")

def test_gasto_descripcion_vacia():
    with pytest.raises(ValueError):
        Gasto(usuario_id="user-1", descripcion="", monto=10, categoria="otro")

def test_gasto_categoria_invalida():
    with pytest.raises(ValueError):
        Gasto(usuario_id="user-1", descripcion="Test", monto=10, categoria="invalida")
```

### tests/unit/test_presupuesto.py
```python
import pytest
from domain.entities import Presupuesto

def test_presupuesto_valido():
    p = Presupuesto(usuario_id="user-1", monto=1000.0, mes=7, anio=2026)
    assert p.monto == 1000.0

def test_presupuesto_monto_negativo():
    with pytest.raises(ValueError):
        Presupuesto(usuario_id="user-1", monto=-100, mes=7, anio=2026)

def test_presupuesto_monto_cero():
    with pytest.raises(ValueError):
        Presupuesto(usuario_id="user-1", monto=0, mes=7, anio=2026)
```

### tests/integration/test_api.py
```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_exitoso():
    response = client.post("/auth/login", json={
        "correo": "biryu@admin.com",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_credenciales_incorrectas():
    response = client.post("/auth/login", json={
        "correo": "biryu@admin.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401

def test_registro_usuario_casual():
    response = client.post("/auth/registro", json={
        "nombre": "Test User",
        "correo": "test_nuevo@test.com",
        "password": "test123"
    })
    assert response.status_code in [200, 201]

def test_acceso_sin_token():
    response = client.get("/gastos/")
    assert response.status_code == 403

def test_admin_listar_usuarios():
    login = client.post("/auth/login", json={
        "correo": "biryu@admin.com",
        "password": "admin123"
    })
    token = login.json()["token"]
    response = client.get("/admin/usuarios", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
```

### tests/load/test_carga.py
```python
from locust import HttpUser, task, between

class UsuarioGastos(HttpUser):
    wait_time = between(1, 2)
    token = None

    def on_start(self):
        response = self.client.post("/auth/login", json={
            "correo": "prueba@gastosya.com",
            "password": "prueba123"
        })
        if response.status_code == 200:
            self.token = response.json().get("token")

    def get_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    @task(3)
    def registrar_gasto(self):
        self.client.post("/gastos/", json={
            "descripcion": "Gasto de prueba",
            "monto": 10.0,
            "categoria": "otro"
        }, headers=self.get_headers())

    @task(2)
    def listar_gastos(self):
        self.client.get("/gastos/", headers=self.get_headers())

    @task(1)
    def obtener_total(self):
        self.client.get("/gastos/total", headers=self.get_headers())

    @task(1)
    def ver_categorias(self):
        self.client.get("/gastos/categorias", headers=self.get_headers())
```

---

## Requirements

```
fastapi==0.111.0
uvicorn==0.29.0
pydantic==2.7.1
sqlalchemy==2.0.30
psycopg2-binary==2.9.9
bcrypt==4.1.3
pyjwt==2.8.0
pytest==8.2.0
httpx==0.27.0
locust==2.28.0
python-multipart==0.0.9
```

---

## Orchestration

Ejecutar en este orden estricto:

1. Eliminar todas las tablas existentes en PostgreSQL (DROP TABLE IF EXISTS gastos, presupuestos, usuarios CASCADE).
2. Crear la estructura de carpetas segun Directives.
3. Implementar domain/entities.py con las tres entidades.
4. Implementar domain/repositories.py con las interfaces.
5. Implementar infrastructure/database.py.
6. Implementar infrastructure/models.py con los tres modelos ORM.
7. Implementar los tres repositorios en infrastructure/.
8. Implementar todos los casos de uso en use_cases/.
9. Implementar api/dependencies.py con JWT.
10. Implementar api/schemas.py con todos los modelos Pydantic.
11. Implementar api/routers/auth.py.
12. Implementar api/routers/gastos.py.
13. Implementar api/routers/presupuesto.py.
14. Implementar api/routers/admin.py.
15. Implementar main.py con seed de usuarios iniciales.
16. Crear index.html con login y registro.
17. Crear usuario.html con las 5 pestanas.
18. Crear admin.html con las 4 pestanas.
19. Crear todos los archivos de pruebas.
20. Actualizar requirements.txt.
21. Ejecutar: pip install -r requirements.txt
22. Ejecutar: uvicorn main:app --reload
23. Verificar que la app corre en http://localhost:8000
24. Ejecutar pruebas: pytest tests/unit/ tests/integration/ -v
25. Confirmar que todas las pruebas pasan.

---

## Como usar el sistema

### Credenciales iniciales:

**Administrador:**
- Correo: biryu@admin.com
- Contrasena: admin123

**Usuario de prueba:**
- Correo: prueba@gastosya.com
- Contrasena: prueba123

### Flujo de uso:
1. Abrir http://localhost:8000
2. Iniciar sesion con las credenciales correspondientes
3. Admin → redirige a /admin-panel
4. Casual → redirige a /dashboard
5. Nuevos usuarios pueden registrarse desde la pantalla de login (rol casual automatico)
