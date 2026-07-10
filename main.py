from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from api.routers.gastos import router
from infrastructure.database import engine, Base
import infrastructure.models  # noqa

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="GastosYa",
    description="Gestor simple de gastos personales",
    version="1.0.0"
)

# Permitir CORS para facilitar el desarrollo frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/", response_class=HTMLResponse)
def inicio():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
            <head><title>GastosYa</title></head>
            <body style="font-family: sans-serif; text-align: center; padding: 50px; background: #0b0f19; color: white;">
                <h1>GastosYa</h1>
                <p>Archivo index.html no encontrado. Por favor créalo en la raíz del proyecto.</p>
            </body>
        </html>
        """

