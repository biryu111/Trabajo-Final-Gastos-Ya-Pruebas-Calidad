# GastosYa — Gestor de Gastos Personales

Aplicación web simple para registrar, listar y eliminar gastos personales.
Permite al usuario llevar un control básico de sus gastos con categoría y monto.
Construida con Python, FastAPI y arquitectura limpia (Clean Architecture).

## Estructura del Proyecto

```text
gastosya/
├── main.py                  # Punto de entrada de la aplicación
├── requirements.txt         # Dependencias del proyecto
├── README.md                # Documentación del proyecto
│
├── domain/                  # Capa de dominio (entidades y reglas de negocio)
│   ├── __init__.py
│   ├── entities.py          # Entidad Gasto
│   └── repositories.py      # Interfaz del repositorio (contrato)
│
├── use_cases/               # Capa de casos de uso (lógica de aplicación)
│   ├── __init__.py
│   ├── agregar_gasto.py
│   ├── listar_gastos.py
│   ├── eliminar_gasto.py
│   └── obtener_total.py
│
├── infrastructure/          # Capa de infraestructura (implementación concreta)
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

## Instalación y Ejecución

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Correr la API:**
   ```bash
   uvicorn main:app --reload
   ```

3. **Ver documentación interactiva:**
   Abrir en navegador: [http://localhost:8000/docs](http://localhost:8000/docs)

4. **Pruebas unitarias:**
   ```bash
   pytest tests/unit/ -v
   ```

5. **Pruebas de integración:**
   ```bash
   pytest tests/integration/ -v
   ```

6. **Pruebas de carga (requiere app corriendo):**
   ```bash
   locust -f tests/load/test_carga.py --host=http://localhost:8000
   ```
