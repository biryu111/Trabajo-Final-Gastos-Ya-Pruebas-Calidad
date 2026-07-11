from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List
from api.schemas import GastoRequest, GastoResponse, TotalResponse, CategoriaResumenItem
from api.dependencies import get_current_user
from use_cases.gastos.agregar_gasto import AgregarGasto
from use_cases.gastos.listar_gastos import ListarGastos
from use_cases.gastos.eliminar_gasto import EliminarGasto
from use_cases.gastos.obtener_total import ObtenerTotal
from use_cases.gastos.listar_gastos_eliminados import ListarGastosEliminados
from use_cases.gastos.obtener_totales_categoria import ObtenerTotalesCategoria
from infrastructure.repositorio_gasto import RepositorioGasto

router = APIRouter(prefix="/gastos", tags=["Gastos"])
repo_gasto = RepositorioGasto()

@router.post("/", response_model=GastoResponse, status_code=201)
def registrar_gasto(data: GastoRequest, current_user: dict = Depends(get_current_user)):
    caso_uso = AgregarGasto(repo_gasto)
    g = caso_uso.ejecutar(current_user["sub"], data.descripcion, data.monto, data.categoria)
    return GastoResponse(
        id=g.id,
        usuario_id=g.usuario_id,
        descripcion=g.descripcion,
        monto=g.monto,
        categoria=g.categoria,
        eliminado=g.eliminado,
        created_at=g.created_at,
        deleted_at=g.deleted_at
    )

@router.get("/", response_model=List[GastoResponse])
def listar_gastos(categoria: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    caso_uso = ListarGastos(repo_gasto)
    gastos = caso_uso.ejecutar(current_user["sub"])
    if categoria:
        gastos = [g for g in gastos if g.categoria == categoria]
    return [
        GastoResponse(
            id=g.id,
            usuario_id=g.usuario_id,
            descripcion=g.descripcion,
            monto=g.monto,
            categoria=g.categoria,
            eliminado=g.eliminado,
            created_at=g.created_at,
            deleted_at=g.deleted_at
        )
        for g in gastos
    ]

@router.delete("/{id}", status_code=204)
def eliminar_gasto(id: str, current_user: dict = Depends(get_current_user)):
    caso_uso = EliminarGasto(repo_gasto)
    # Los usuarios casuales solo pueden borrar sus propios gastos
    eliminado = caso_uso.ejecutar(id, current_user["sub"])
    if not eliminado:
        raise HTTPException(status_code=404, detail="Gasto no encontrado.")

@router.get("/total", response_model=TotalResponse)
def obtener_total(current_user: dict = Depends(get_current_user)):
    caso_uso = ObtenerTotal(repo_gasto)
    total = caso_uso.ejecutar(current_user["sub"])
    return TotalResponse(total=total)

@router.get("/eliminados", response_model=List[GastoResponse])
def listar_gastos_eliminados(current_user: dict = Depends(get_current_user)):
    caso_uso = ListarGastosEliminados(repo_gasto)
    gastos = caso_uso.ejecutar(current_user["sub"])
    return [
        GastoResponse(
            id=g.id,
            usuario_id=g.usuario_id,
            descripcion=g.descripcion,
            monto=g.monto,
            categoria=g.categoria,
            eliminado=g.eliminado,
            created_at=g.created_at,
            deleted_at=g.deleted_at
        )
        for g in gastos
    ]

@router.get("/categorias", response_model=List[CategoriaResumenItem])
def obtener_totales_categoria(current_user: dict = Depends(get_current_user)):
    caso_uso_totales = ObtenerTotalesCategoria(repo_gasto)
    caso_uso_total = ObtenerTotal(repo_gasto)
    
    totales = caso_uso_totales.ejecutar(current_user["sub"])
    total_general = caso_uso_total.ejecutar(current_user["sub"])
    
    resumen = []
    for cat, monto in totales.items():
        porcentaje = (monto / total_general * 100) if total_general > 0 else 0.0
        resumen.append(
            CategoriaResumenItem(
                categoria=cat,
                total=monto,
                porcentaje=round(porcentaje, 2)
            )
        )
    return resumen
