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
    assert response.status_code in [401, 403]

def test_admin_listar_usuarios():
    login = client.post("/auth/login", json={
        "correo": "biryu@admin.com",
        "password": "admin123"
    })
    token = login.json()["token"]
    response = client.get("/admin/usuarios", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
