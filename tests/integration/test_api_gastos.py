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
