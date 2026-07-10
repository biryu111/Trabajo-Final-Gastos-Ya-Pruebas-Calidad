# GastosYa — Gestor de Gastos Personales

## Descripcion del proyecto

Aplicacion web simple para registrar, listar y eliminar gastos personales.
Permite al usuario llevar un control basico de sus gastos con categoria y monto.
Construida con Python, FastAPI y arquitectura limpia (Clean Architecture).

---

## Directives

```
gastosya/
├── main.py                  # Punto de entrada de la aplicacion
├── requirements.txt         # Dependencias del proyecto
├── README.md                # Documentacion del proyecto
│
├── domain/                  # Capa de dominio (entidades y reglas de negocio)
│   ├── __init__.py
│   ├── entities.py          # Entidad Gasto
│   └── repositories.py     # Interfaz del repositorio (contrato)
│
├── use_cases/               # Capa de casos de uso (logica de aplicacion)
│   ├── __init__.py
│   ├── agregar_gasto.py
│   ├── listar_gastos.py
│   ├── eliminar_gasto.py
│   └── obtener_total.py
│
├── infrastructure/          # Capa de infraestructura (implementacion concreta)
│   ├── __init__.py
│   └── repositorio_memoria.py  # Repositorio en memoria (lista Python)
│
├── api/                     # Capa de API (FastAPI - controladores)
│   ├── __init__.py
│   ├── routers/
│   │   └── gastos.py        # Endpoints REST
│   └── schemas.py           # Modelos Pydantic (request/response)
│
└── tests/                   # Pruebas
    ├── __init__.py
    ├── unit/
    │   ├── __init__.py
    │   ├── test_agregar_gasto.py
    │   ├── test_listar_gastos.py
    │   ├── test_eliminar_gasto.py
    │   └── test_obtener_total.py
    ├── integration/
    │   ├── __init__.py
    │   └── test_api_gastos.py
    └── load/
        ├── __init__.py
        └── test_carga.py
```

---

## Analisis de Requisitos

### Historias de Usuario

#### HU-01 — Registrar Gasto
**Como** usuario
**quiero** registrar un gasto con descripcion, monto y categoria
**para** llevar control de mis gastos personales.

**Criterios de aceptacion:**
- CA-01: El monto debe ser mayor a cero.
- CA-02: La descripcion no puede estar vacia.
- CA-03: La categoria debe ser una de las permitidas: alimentacion, transporte, salud, entretenimiento, otro.
- CA-04: El gasto debe quedar registrado con un ID unico.

#### HU-02 — Listar Gastos
**Como** usuario
**quiero** ver todos mis gastos registrados
**para** revisar en que he gastado.

**Criterios de aceptacion:**
- CA-01: El sistema debe retornar la lista completa de gastos.
- CA-02: Si no hay gastos, debe retornar una lista vacia.

#### HU-03 — Eliminar Gasto
**Como** usuario
**quiero** eliminar un gasto registrado
**para** corregir errores de registro.

**Criterios de aceptacion:**
- CA-01: El gasto debe existir para poder eliminarlo.
- CA-02: Si el ID no existe, el sistema debe retornar un error claro.

#### HU-04 — Consultar Total Gastado
**Como** usuario
**quiero** ver el total de mis gastos
**para** saber cuanto he gastado en total.

**Criterios de aceptacion:**
- CA-01: El total debe ser la suma de todos los montos registrados.
- CA-02: Si no hay gastos, el total debe ser 0.

---

## Reglas de Negocio

| ID | Regla |
|----|-------|
| RN-01 | El monto de un gasto debe ser estrictamente mayor a cero. |
| RN-02 | La descripcion no puede ser una cadena vacia o solo espacios. |
| RN-03 | La categoria debe pertenecer al conjunto definido. |
| RN-04 | Cada gasto tiene un ID unico autogenerado (UUID). |
| RN-05 | No se puede eliminar un gasto con ID inexistente. |

---

## Arquitectura — Clean Architecture

### Capas

```
[ API Layer ]         <-- FastAPI routers y schemas (entrada HTTP)
      |
[ Use Cases ]         <-- Logica de negocio de la aplicacion
      |
[ Domain ]            <-- Entidades y contratos (interfaces)
      |
[ Infrastructure ]    <-- Implementacion concreta (repositorio en memoria)
```

### Principios aplicados
- **Dependency Inversion**: Los casos de uso dependen de interfaces, no de implementaciones.
- **Single Responsibility**: Cada caso de uso hace una sola cosa.
- **Separation of Concerns**: La API no conoce la logica de negocio directamente.

---

## Endpoints REST

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| POST | /gastos | Registrar un nuevo gasto |
| GET | /gastos | Listar todos los gastos |
| DELETE | /gastos/{id} | Eliminar un gasto por ID |
| GET | /gastos/total | Obtener el total gastado |

---

## Modelos de Datos

### Request — Crear Gasto
```json
{
  "descripcion": "Almuerzo",
  "monto": 15.50,
  "categoria": "alimentacion"
}
```

### Response — Gasto creado
```json
{
  "id": "uuid-generado",
  "descripcion": "Almuerzo",
  "monto": 15.50,
  "categoria": "alimentacion"
}
```

### Response — Total
```json
{
  "total": 45.50
}
```

---

## Stack Tecnologico

| Componente | Tecnologia |
|------------|------------|
| Lenguaje | Python 3.11+ |
| Framework API | FastAPI |
| Validacion | Pydantic v2 |
| Servidor | Uvicorn |
| Pruebas unitarias | pytest |
| Pruebas de integracion | pytest + httpx |
| Pruebas de carga | locust |
| Repositorio | En memoria (lista Python) |

---

## Dependencias — requirements.txt

```
fastapi==0.111.0
uvicorn==0.29.0
pydantic==2.7.1
pytest==8.2.0
httpx==0.27.0
locust==2.28.0
```

---

## Implementacion

### domain/entities.py
```python
from dataclasses import dataclass, field
from uuid import uuid4

CATEGORIAS_PERMITIDAS = {"alimentacion", "transporte", "salud", "entretenimiento", "otro"}

@dataclass
class Gasto:
    descripcion: str
    monto: float
    categoria: str
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        if self.monto <= 0:
            raise ValueError("El monto debe ser mayor a cero.")
        if not self.descripcion or not self.descripcion.strip():
            raise ValueError("La descripcion no puede estar vacia.")
        if self.categoria not in CATEGORIAS_PERMITIDAS:
            raise ValueError(f"Categoria invalida. Permitidas: {CATEGORIAS_PERMITIDAS}")
```

### domain/repositories.py
```python
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import Gasto

class GastoRepository(ABC):

    @abstractmethod
    def agregar(self, gasto: Gasto) -> Gasto:
        pass

    @abstractmethod
    def listar(self) -> List[Gasto]:
        pass

    @abstractmethod
    def eliminar(self, id: str) -> bool:
        pass

    @abstractmethod
    def obtener_total(self) -> float:
        pass
```

### infrastructure/repositorio_memoria.py
```python
from typing import List
from domain.entities import Gasto
from domain.repositories import GastoRepository

class RepositorioMemoria(GastoRepository):

    def __init__(self):
        self._gastos: List[Gasto] = []

    def agregar(self, gasto: Gasto) -> Gasto:
        self._gastos.append(gasto)
        return gasto

    def listar(self) -> List[Gasto]:
        return list(self._gastos)

    def eliminar(self, id: str) -> bool:
        for i, g in enumerate(self._gastos):
            if g.id == id:
                self._gastos.pop(i)
                return True
        return False

    def obtener_total(self) -> float:
        return sum(g.monto for g in self._gastos)
```

### use_cases/agregar_gasto.py
```python
from domain.entities import Gasto
from domain.repositories import GastoRepository

class AgregarGasto:

    def __init__(self, repo: GastoRepository):
        self.repo = repo

    def ejecutar(self, descripcion: str, monto: float, categoria: str) -> Gasto:
        gasto = Gasto(descripcion=descripcion, monto=monto, categoria=categoria)
        return self.repo.agregar(gasto)
```

### use_cases/listar_gastos.py
```python
from typing import List
from domain.entities import Gasto
from domain.repositories import GastoRepository

class ListarGastos:

    def __init__(self, repo: GastoRepository):
        self.repo = repo

    def ejecutar(self) -> List[Gasto]:
        return self.repo.listar()
```

### use_cases/eliminar_gasto.py
```python
from domain.repositories import GastoRepository

class EliminarGasto:

    def __init__(self, repo: GastoRepository):
        self.repo = repo

    def ejecutar(self, id: str) -> bool:
        return self.repo.eliminar(id)
```

### use_cases/obtener_total.py
```python
from domain.repositories import GastoRepository

class ObtenerTotal:

    def __init__(self, repo: GastoRepository):
        self.repo = repo

    def ejecutar(self) -> float:
        return self.repo.obtener_total()
```

### api/schemas.py
```python
from pydantic import BaseModel, field_validator
from domain.entities import CATEGORIAS_PERMITIDAS

class GastoRequest(BaseModel):
    descripcion: str
    monto: float
    categoria: str

    @field_validator("monto")
    @classmethod
    def monto_positivo(cls, v):
        if v <= 0:
            raise ValueError("El monto debe ser mayor a cero.")
        return v

    @field_validator("descripcion")
    @classmethod
    def descripcion_no_vacia(cls, v):
        if not v or not v.strip():
            raise ValueError("La descripcion no puede estar vacia.")
        return v

    @field_validator("categoria")
    @classmethod
    def categoria_valida(cls, v):
        if v not in CATEGORIAS_PERMITIDAS:
            raise ValueError(f"Categoria invalida. Permitidas: {CATEGORIAS_PERMITIDAS}")
        return v

class GastoResponse(BaseModel):
    id: str
    descripcion: str
    monto: float
    categoria: str

class TotalResponse(BaseModel):
    total: float
```

### api/routers/gastos.py
```python
from fastapi import APIRouter, HTTPException
from api.schemas import GastoRequest, GastoResponse, TotalResponse
from use_cases.agregar_gasto import AgregarGasto
from use_cases.listar_gastos import ListarGastos
from use_cases.eliminar_gasto import EliminarGasto
from use_cases.obtener_total import ObtenerTotal
from infrastructure.repositorio_memoria import RepositorioMemoria

router = APIRouter(prefix="/gastos", tags=["Gastos"])
repo = RepositorioMemoria()

@router.post("/", response_model=GastoResponse, status_code=201)
def registrar_gasto(data: GastoRequest):
    caso_uso = AgregarGasto(repo)
    gasto = caso_uso.ejecutar(data.descripcion, data.monto, data.categoria)
    return GastoResponse(id=gasto.id, descripcion=gasto.descripcion,
                         monto=gasto.monto, categoria=gasto.categoria)

@router.get("/", response_model=list[GastoResponse])
def listar_gastos():
    caso_uso = ListarGastos(repo)
    gastos = caso_uso.ejecutar()
    return [GastoResponse(id=g.id, descripcion=g.descripcion,
                          monto=g.monto, categoria=g.categoria) for g in gastos]

@router.delete("/{id}", status_code=204)
def eliminar_gasto(id: str):
    caso_uso = EliminarGasto(repo)
    eliminado = caso_uso.ejecutar(id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Gasto no encontrado.")

@router.get("/total", response_model=TotalResponse)
def obtener_total():
    caso_uso = ObtenerTotal(repo)
    total = caso_uso.ejecutar()
    return TotalResponse(total=total)
```

### main.py
```python
from fastapi import FastAPI
from api.routers.gastos import router

app = FastAPI(
    title="GastosYa",
    description="Gestor simple de gastos personales",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a GastosYa"}
```

---

## Pruebas

### tests/unit/test_agregar_gasto.py
```python
import pytest
from use_cases.agregar_gasto import AgregarGasto
from infrastructure.repositorio_memoria import RepositorioMemoria

def test_agregar_gasto_valido():
    repo = RepositorioMemoria()
    caso_uso = AgregarGasto(repo)
    gasto = caso_uso.ejecutar("Almuerzo", 15.50, "alimentacion")
    assert gasto.descripcion == "Almuerzo"
    assert gasto.monto == 15.50
    assert gasto.categoria == "alimentacion"
    assert gasto.id is not None

def test_agregar_gasto_monto_invalido():
    repo = RepositorioMemoria()
    caso_uso = AgregarGasto(repo)
    with pytest.raises(ValueError):
        caso_uso.ejecutar("Almuerzo", -10, "alimentacion")

def test_agregar_gasto_descripcion_vacia():
    repo = RepositorioMemoria()
    caso_uso = AgregarGasto(repo)
    with pytest.raises(ValueError):
        caso_uso.ejecutar("", 10, "alimentacion")

def test_agregar_gasto_categoria_invalida():
    repo = RepositorioMemoria()
    caso_uso = AgregarGasto(repo)
    with pytest.raises(ValueError):
        caso_uso.ejecutar("Cine", 20, "diversión")
```

### tests/unit/test_listar_gastos.py
```python
from use_cases.agregar_gasto import AgregarGasto
from use_cases.listar_gastos import ListarGastos
from infrastructure.repositorio_memoria import RepositorioMemoria

def test_listar_gastos_vacio():
    repo = RepositorioMemoria()
    caso_uso = ListarGastos(repo)
    assert caso_uso.ejecutar() == []

def test_listar_gastos_con_datos():
    repo = RepositorioMemoria()
    AgregarGasto(repo).ejecutar("Bus", 2.50, "transporte")
    AgregarGasto(repo).ejecutar("Medicina", 30.0, "salud")
    gastos = ListarGastos(repo).ejecutar()
    assert len(gastos) == 2
```

### tests/unit/test_eliminar_gasto.py
```python
from use_cases.agregar_gasto import AgregarGasto
from use_cases.eliminar_gasto import EliminarGasto
from infrastructure.repositorio_memoria import RepositorioMemoria

def test_eliminar_gasto_existente():
    repo = RepositorioMemoria()
    gasto = AgregarGasto(repo).ejecutar("Taxi", 10.0, "transporte")
    resultado = EliminarGasto(repo).ejecutar(gasto.id)
    assert resultado is True

def test_eliminar_gasto_inexistente():
    repo = RepositorioMemoria()
    resultado = EliminarGasto(repo).ejecutar("id-que-no-existe")
    assert resultado is False
```

### tests/unit/test_obtener_total.py
```python
from use_cases.agregar_gasto import AgregarGasto
from use_cases.obtener_total import ObtenerTotal
from infrastructure.repositorio_memoria import RepositorioMemoria

def test_total_sin_gastos():
    repo = RepositorioMemoria()
    assert ObtenerTotal(repo).ejecutar() == 0

def test_total_con_gastos():
    repo = RepositorioMemoria()
    AgregarGasto(repo).ejecutar("Almuerzo", 15.0, "alimentacion")
    AgregarGasto(repo).ejecutar("Bus", 2.50, "transporte")
    assert ObtenerTotal(repo).ejecutar() == 17.50
```

### tests/integration/test_api_gastos.py
```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_registrar_gasto():
    response = client.post("/gastos/", json={
        "descripcion": "Almuerzo",
        "monto": 15.50,
        "categoria": "alimentacion"
    })
    assert response.status_code == 201
    assert response.json()["descripcion"] == "Almuerzo"

def test_listar_gastos():
    response = client.get("/gastos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_eliminar_gasto_existente():
    post = client.post("/gastos/", json={
        "descripcion": "Taxi",
        "monto": 10.0,
        "categoria": "transporte"
    })
    id_gasto = post.json()["id"]
    response = client.delete(f"/gastos/{id_gasto}")
    assert response.status_code == 204

def test_eliminar_gasto_inexistente():
    response = client.delete("/gastos/id-falso-123")
    assert response.status_code == 404

def test_obtener_total():
    response = client.get("/gastos/total")
    assert response.status_code == 200
    assert "total" in response.json()
```

### tests/load/test_carga.py
```python
from locust import HttpUser, task, between

class UsuarioGastos(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def registrar_gasto(self):
        self.client.post("/gastos/", json={
            "descripcion": "Gasto de prueba",
            "monto": 10.0,
            "categoria": "otro"
        })

    @task(2)
    def listar_gastos(self):
        self.client.get("/gastos/")

    @task(1)
    def obtener_total(self):
        self.client.get("/gastos/total")
```

---

## Orchestration

Ejecutar en este orden estricto:

1. Crear la estructura de carpetas segun Directives.
2. Crear todos los archivos de dominio (entities.py, repositories.py).
3. Crear la infraestructura (repositorio_memoria.py).
4. Crear los casos de uso (agregar, listar, eliminar, obtener_total).
5. Crear los schemas y routers de la API.
6. Crear el main.py.
7. Crear el requirements.txt.
8. Crear todos los archivos de pruebas.
9. Verificar que la app corre con: uvicorn main:app --reload
10. Ejecutar pruebas unitarias: pytest tests/unit/
11. Ejecutar pruebas de integracion: pytest tests/integration/
12. Ejecutar pruebas de carga: locust -f tests/load/test_carga.py

---

## Como correr el proyecto manualmente

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Correr la API
uvicorn main:app --reload

# 3. Ver documentacion interactiva
# Abrir en navegador: http://localhost:8000/docs

# 4. Pruebas unitarias
pytest tests/unit/ -v

# 5. Pruebas de integracion
pytest tests/integration/ -v

# 6. Pruebas de carga (requiere app corriendo)
locust -f tests/load/test_carga.py --host=http://localhost:8000
```
