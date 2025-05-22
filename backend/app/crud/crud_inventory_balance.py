from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.inventory_balance import InventoryBalance as InventoryBalanceModel
from app.schemas.inventory_balance import InventoryBalanceCreate, InventoryBalanceUpdate

# 根据物资ID获取库存余額
def get_inventory_balance_by_material_id(db: Session, material_id: int) -> InventoryBalanceModel | None:
    return db.query(InventoryBalanceModel).filter(InventoryBalanceModel.material_id == material_id).first()

# 创建库存余額 (通常在创建物资时调用)
def create_inventory_balance(db: Session, inventory_balance: InventoryBalanceCreate) -> InventoryBalanceModel:
    # 检查该物资是否已存在库存记录
    existing_balance = get_inventory_balance_by_material_id(db, material_id=inventory_balance.material_id)
    if existing_balance:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"物资ID {inventory_balance.material_id} 的库存记录已存在。"
        )
    
    db_inventory_balance = InventoryBalanceModel(**inventory_balance.model_dump())
    db.add(db_inventory_balance)
    try:
        db.commit()
        db.refresh(db_inventory_balance)
    except IntegrityError: # 捕获可能的数据库层面完整性错误 (例如外键约束失败)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无法为物资ID {inventory_balance.material_id} 创建库存记录，请检查物资是否存在。"
        )
    return db_inventory_balance

# 更新库存余額 (核心操作，由入库/出库逻辑调用，或手动调整)
def update_inventory_balance_quantity(
    db: Session,
    material_id: int,
    quantity_change: int, # 正数表示增加 (入库)，负数表示减少 (出库)
    is_adjustment: bool = False # 标记是否为手动调整，手动调整时不检查出库库存
) -> InventoryBalanceModel:
    db_inventory_balance = get_inventory_balance_by_material_id(db, material_id=material_id)
    if not db_inventory_balance:
        # 如果物资没有库存记录 (理论上不应发生，因为创建物资时应初始化库存)
        # 可以选择在这里自动创建一条，或者抛出错误
        # 为了简化，这里假设物资创建时已确保有库存记录
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"物资ID {material_id} 的库存记录未找到，无法更新数量。"
        )

    if not is_adjustment and quantity_change < 0: # 如果是出库操作
        if db_inventory_balance.current_quantity + quantity_change < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"物资ID {material_id} 库存不足。当前库存: {db_inventory_balance.current_quantity}, 需出库: {-quantity_change}"
            )
    
    db_inventory_balance.current_quantity += quantity_change
    db.add(db_inventory_balance) # SQLAlchemy 会识别为更新
    db.commit()
    db.refresh(db_inventory_balance)
    return db_inventory_balance

# 管理员手动更新库存余額的详细信息 (不仅仅是数量)
def update_inventory_balance_details(db: Session, material_id: int, inventory_update: InventoryBalanceUpdate) -> InventoryBalanceModel | None:
    db_inventory_balance = get_inventory_balance_by_material_id(db, material_id=material_id)
    if not db_inventory_balance:
        return None

    update_data = inventory_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_inventory_balance, key, value)
    
    db.add(db_inventory_balance)
    db.commit()
    db.refresh(db_inventory_balance)
    return db_inventory_balance


# 获取库存余額列表 (可分页)
def get_inventory_balances(db: Session, skip: int = 0, limit: int = 100) -> list[InventoryBalanceModel]:
    return db.query(InventoryBalanceModel).offset(skip).limit(limit).all()

# (可选) 根据ID获取库存余額记录 (虽然通常按 material_id 查询)
def get_inventory_balance_by_id(db: Session, balance_id: int) -> InventoryBalanceModel | None:
    return db.query(InventoryBalanceModel).filter(InventoryBalanceModel.id == balance_id).first()