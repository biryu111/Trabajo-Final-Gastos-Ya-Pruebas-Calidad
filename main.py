from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
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

# Permitir CORS para desarrollo local flexible
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
            hashed = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
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
            hashed = bcrypt.hashpw("prueba123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
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
