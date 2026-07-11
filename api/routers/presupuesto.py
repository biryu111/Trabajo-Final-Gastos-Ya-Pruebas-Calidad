from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from api.schemas import PresupuestoRequest, PresupuestoResponse, PresupuestoEstadoResponse
from api.dependencies import get_current_user
from use_cases.presupuesto.gestionar_presupuesto import GestionarPresupuesto
from use_cases.gastos.obtener_total import ObtenerTotal
from infrastructure.repositorio_presupuesto import RepositorioPresupuesto
from infrastructure.repositorio_gasto import RepositorioGasto

router = APIRouter(prefix="/presupuesto", tags=["Presupuesto"])
repo_presupuesto = RepositorioPresupuesto()
repo_gasto = RepositorioGasto()

@router.post("/", response_model=PresupuestoResponse, status_code=201)
def definir_presupuesto(data: PresupuestoRequest, current_user: dict = Depends(get_current_user)):
    caso_uso = GestionarPresupuesto(repo_presupuesto)
    p = caso_uso.definir(current_user["sub"], data.monto, data.mes, data.anio)
    return PresupuestoResponse(
        id=p.id,
        usuario_id=p.usuario_id,
        monto=p.monto,
        mes=p.mes,
        anio=p.anio
    )

@router.get("/", response_model=PresupuestoEstadoResponse)
def obtener_presupuesto_estado(current_user: dict = Depends(get_current_user)):
    now = datetime.now()
    mes_actual = now.month
    anio_actual = now.year

    caso_uso_pres = GestionarPresupuesto(repo_presupuesto)
    caso_uso_gasto = ObtenerTotal(repo_gasto)

    p = caso_uso_pres.obtener(current_user["sub"], mes_actual, anio_actual)
    total_gastado = caso_uso_gasto.ejecutar(current_user["sub"])

    presupuesto_monto = p.monto if p else None
    
    saldo_restante = 0.0
    superado = False
    if presupuesto_monto is not None:
        saldo_restante = presupuesto_monto - total_gastado
        superado = total_gastado > presupuesto_monto
    
    return PresupuestoEstadoResponse(
        presupuesto=presupuesto_monto,
        total_gastado=total_gastado,
        saldo_restante=saldo_restante,
        superado=superado
    )

@router.put("/", response_model=PresupuestoResponse)
def actualizar_presupuesto(data: PresupuestoRequest, current_user: dict = Depends(get_current_user)):
    caso_uso = GestionarPresupuesto(repo_presupuesto)
    p = caso_uso.definir(current_user["sub"], data.monto, data.mes, data.anio)
    return PresupuestoResponse(
        id=p.id,
        usuario_id=p.usuario_id,
        monto=p.monto,
        mes=p.mes,
        anio=p.anio
    )
