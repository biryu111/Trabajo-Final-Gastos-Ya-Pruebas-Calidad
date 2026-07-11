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
