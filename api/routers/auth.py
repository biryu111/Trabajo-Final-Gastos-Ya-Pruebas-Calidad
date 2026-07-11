from fastapi import APIRouter, HTTPException, Depends
from api.schemas import LoginRequest, LoginResponse, RegistroRequest, RegistroResponse, UserMeResponse
from api.dependencies import get_current_user
from use_cases.auth.login import Login
from use_cases.auth.registrar_usuario import RegistrarUsuario
from use_cases.auth.obtener_usuario import ObtenerUsuario
from infrastructure.repositorio_usuario import RepositorioUsuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])
repo_usuario = RepositorioUsuario()

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):
    try:
        caso_uso = Login(repo_usuario)
        token = caso_uso.ejecutar(data.correo, data.password)
        return LoginResponse(token=token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/registro", response_model=RegistroResponse, status_code=201)
def registro(data: RegistroRequest):
    try:
        caso_uso = RegistrarUsuario(repo_usuario)
        usuario = caso_uso.ejecutar(data.nombre, data.correo, data.password)
        return RegistroResponse(
            id=usuario.id,
            nombre=usuario.nombre,
            correo=usuario.correo,
            rol=usuario.rol,
            activo=usuario.activo
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=UserMeResponse)
def me(current_user: dict = Depends(get_current_user)):
    caso_uso = ObtenerUsuario(repo_usuario)
    usuario = caso_uso.ejecutar(current_user["sub"])
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return UserMeResponse(
        id=usuario.id,
        nombre=usuario.nombre,
        correo=usuario.correo,
        rol=usuario.rol
    )
