from fastapi import APIRouter, HTTPException
from api.schemas import GastoRequest, GastoResponse, TotalResponse
from use_cases.agregar_gasto import AgregarGasto
from use_cases.listar_gastos import ListarGastos
from use_cases.eliminar_gasto import EliminarGasto
from use_cases.obtener_total import ObtenerTotal
from infrastructure.repositorio_db import RepositorioDb

router = APIRouter(prefix="/gastos", tags=["Gastos"])
repo = RepositorioDb()

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
