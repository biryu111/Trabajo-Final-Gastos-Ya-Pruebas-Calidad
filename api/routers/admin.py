from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
from api.schemas import UserAdminResponse, GastoResponse, CategoriaResumenItem, PresupuestoEstadoResponse
from api.dependencies import require_admin
from use_cases.admin.listar_usuarios import ListarUsuarios
from use_cases.admin.eliminar_usuario import EliminarUsuario
from use_cases.admin.ver_gastos_usuario import VerGastosUsuario
from use_cases.gastos.listar_gastos_eliminados import ListarGastosEliminados
from use_cases.gastos.eliminar_gasto import EliminarGasto
from use_cases.gastos.obtener_totales_categoria import ObtenerTotalesCategoria
from infrastructure.repositorio_usuario import RepositorioUsuario
from infrastructure.repositorio_gasto import RepositorioGasto
from infrastructure.repositorio_presupuesto import RepositorioPresupuesto

router = APIRouter(prefix="/admin", tags=["Administración"], dependencies=[Depends(require_admin)])
repo_usuario = RepositorioUsuario()
repo_gasto = RepositorioGasto()
repo_presupuesto = RepositorioPresupuesto()

@router.get("/usuarios", response_model=List[UserAdminResponse])
def listar_usuarios():
    caso_uso = ListarUsuarios(repo_usuario)
    usuarios = caso_uso.ejecutar()
    return [
        UserAdminResponse(
            id=u.id,
            nombre=u.nombre,
            correo=u.correo,
            password=u.password,
            rol=u.rol,
            activo=u.activo,
            created_at=u.created_at
        ) for u in usuarios
    ]

@router.delete("/usuarios/{id}", status_code=204)
def eliminar_usuario(id: str):
    try:
        caso_uso = EliminarUsuario(repo_usuario)
        eliminado = caso_uso.ejecutar(id)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/usuarios/{id}/gastos", response_model=List[GastoResponse])
def ver_gastos_usuario(id: str):
    caso_uso = VerGastosUsuario(repo_gasto)
    gastos = caso_uso.ejecutar(id)
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
        ) for g in gastos
    ]

@router.get("/usuarios/{id}/eliminados", response_model=List[GastoResponse])
def ver_gastos_eliminados_usuario(id: str):
    caso_uso = ListarGastosEliminados(repo_gasto)
    gastos = caso_uso.ejecutar(id)
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
        ) for g in gastos
    ]

@router.delete("/gastos/{id}", status_code=204)
def eliminar_gasto_cualquiera(id: str):
    caso_uso = EliminarGasto(repo_gasto)
    eliminado = caso_uso.ejecutar(id, usuario_id=None)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Gasto no encontrado.")

@router.get("/usuarios/{id}/presupuesto", response_model=PresupuestoEstadoResponse)
def ver_presupuesto_usuario(id: str):
    """Devuelve el estado del presupuesto del mes actual de un usuario específico."""
    now = datetime.now()
    presupuesto = repo_presupuesto.obtener_por_usuario(id, mes=now.month, anio=now.year)
    gastos = repo_gasto.listar(id)
    total_gastado = sum(g.monto for g in gastos)
    if presupuesto:
        saldo = presupuesto.monto - total_gastado
        superado = total_gastado > presupuesto.monto
        return PresupuestoEstadoResponse(
            presupuesto=presupuesto.monto,
            total_gastado=total_gastado,
            saldo_restante=saldo,
            superado=superado
        )
    return PresupuestoEstadoResponse(
        presupuesto=None,
        total_gastado=total_gastado,
        saldo_restante=0.0,
        superado=False
    )

@router.get("/usuarios/{id}/categorias", response_model=List[CategoriaResumenItem])
def ver_categorias_usuario(id: str):
    """Devuelve el desglose de gastos por categoría de un usuario específico."""
    caso_uso_totales = ObtenerTotalesCategoria(repo_gasto)
    totales = caso_uso_totales.ejecutar(id)
    
    # Calcular total general para los porcentajes
    total_general = sum(totales.values())
    
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
