from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import schemas 
from app import crud 
from app.db.database import get_db 

router = APIRouter()

@router.get(
    "/",
    response_model=List[schemas.inventory_balance.InventoryBalance],
    summary="获取库存余額列表 (UC4)",
    description="获取所有物资的当前库存余額信息，支持分页。"
)
def read_inventory_balances(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=200, description="每页返回的记录数"),
    db: Session = Depends(get_db)
):
    balances = crud.crud_inventory_balance.get_inventory_balances(db, skip=skip, limit=limit)
    return balances

@router.get(
    "/material/{material_id}",
    response_model=schemas.inventory_balance.InventoryBalance,
    summary="根据物资ID获取库存余額 (UC4)",
    description="获取指定物资ID的当前库存余額信息。"
)
def read_inventory_balance_for_material(material_id: int, db: Session = Depends(get_db)):
    balance = crud.crud_inventory_balance.get_inventory_balance_by_material_id(db, material_id=material_id)
    if balance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"物资ID {material_id} 的库存记录未找到")
    return balance

@router.put(
    "/material/{material_id}",
    response_model=schemas.inventory_balance.InventoryBalance,
    summary="管理员手动调整物资库存详情 (慎用)",
    description="允许管理员更新指定物资的库存余額详细信息，如最低/最高库存水平，或直接调整当前数量。"
)
def update_material_inventory_balance_details(
    material_id: int,
    inventory_update: schemas.inventory_balance.InventoryBalanceUpdate,
    db: Session = Depends(get_db)
    # current_user: schemas.user.User = Depends(get_current_active_admin_user) # 权限控制
):
    updated_balance = crud.crud_inventory_balance.update_inventory_balance_details(
        db=db, material_id=material_id, inventory_update=inventory_update
    )
    if updated_balance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"物资ID {material_id} 的库存记录未找到")
    return updated_balance

# 创建库存余額的 API 通常不直接暴露，因为它应作为创建物资时的副作用。
# 如果确实需要，可以添加一个 POST 端点，并确保其被适当保护。