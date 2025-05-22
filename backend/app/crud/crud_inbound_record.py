from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.models.inbound_record import InboundRecord as InboundRecordModel
from app.schemas.inbound_record import InboundRecordCreate
from app.crud.crud_inventory_balance import update_inventory_balance_quantity, get_inventory_balance_by_material_id, create_inventory_balance
from app.schemas.inventory_balance import InventoryBalanceCreate
from datetime import datetime

# 创建入库记录，并更新库存余額
def create_inbound_record(db: Session, inbound_record_data: InboundRecordCreate) -> InboundRecordModel:
    try:
        # 步骤 1: 创建入库记录对象并添加到会话
        db_inbound_record = InboundRecordModel(**inbound_record_data.model_dump())
        db.add(db_inbound_record)

        material_id = inbound_record_data.material_id
        quantity_change = inbound_record_data.quantity

        # 步骤 2: 更新或初始化库存余額 (这些函数现在不应自行 commit)
        inventory_balance = get_inventory_balance_by_material_id(db, material_id=material_id)
        if not inventory_balance:
            initial_balance_data = InventoryBalanceCreate(
                material_id=material_id,
                current_quantity=0 
            )
            # create_inventory_balance 现在不 commit，只 add
            created_balance = create_inventory_balance(db=db, inventory_balance=initial_balance_data) 
            if not created_balance: # 假设 create_inventory_balance 在错误时返回 None 或抛错
                raise Exception("Failed to initialize inventory balance.")


        # update_inventory_balance_quantity 现在不 commit，只 add (或修改对象)
        updated_inv = update_inventory_balance_quantity(db=db, material_id=material_id, quantity_change=quantity_change)
        if not updated_inv: # 假设 update_inventory_balance_quantity 在错误时返回 None 或抛错
            raise Exception("Failed to update inventory quantity.")


        # 步骤 3: 所有操作成功后，统一提交事务
        db.commit()
        db.refresh(db_inbound_record) # 刷新以获取数据库生成的值
        # 如果需要，也可以刷新 inventory_balance
        # db.refresh(updated_inv if updated_inv else created_balance)

        return db_inbound_record

    except HTTPException: # 直接重新抛出已知的业务逻辑异常
        db.rollback()
        raise
    except SQLAlchemyError as e_sql: # 捕获所有 SQLAlchemy 错误
        db.rollback()
        print(f"Database error during inbound record creation: {e_sql}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database operation failed: {e_sql}"
        )
    except Exception as e_global: # 捕获其他所有意外错误
        db.rollback()
        print(f"Unexpected error during inbound record creation: {e_global}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e_global}"
        )

# 根据ID获取入库记录
def get_inbound_record_by_id(db: Session, record_id: int) -> InboundRecordModel | None:
    return db.query(InboundRecordModel).filter(InboundRecordModel.id == record_id).first()

# 获取入库记录列表 (可分页、可按物资ID、时间范围等过滤)
def get_inbound_records(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    material_id: int | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None
) -> list[InboundRecordModel]:
    query = db.query(InboundRecordModel)
    if material_id is not None:
        query = query.filter(InboundRecordModel.material_id == material_id)
    if start_time:
        query = query.filter(InboundRecordModel.inbound_time >= start_time)
    if end_time:
        query = query.filter(InboundRecordModel.inbound_time <= end_time)
    return query.order_by(InboundRecordModel.inbound_time.desc()).offset(skip).limit(limit).all()