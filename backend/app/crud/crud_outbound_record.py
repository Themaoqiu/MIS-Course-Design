from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.outbound_record import OutboundRecord as OutboundRecordModel
from app.schemas.outbound_record import OutboundRecordCreate
from app.crud.crud_inventory_balance import update_inventory_balance_quantity, get_inventory_balance_by_material_id
from datetime import datetime

# 创建出库记录，并更新库存余額 (先检查库存)
def create_outbound_record(db: Session, outbound_record_data: OutboundRecordCreate) -> OutboundRecordModel:
    material_id = outbound_record_data.material_id
    quantity_to_outbound = outbound_record_data.quantity

    # 1. 检查库存是否充足 (这一步已包含在 update_inventory_balance_quantity 中，但明确写出更好)
    # inventory_balance = get_inventory_balance_by_material_id(db, material_id=material_id)
    # if not inventory_balance or inventory_balance.current_quantity < quantity_to_outbound:
    #     current_stock = inventory_balance.current_quantity if inventory_balance else 0
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"物资ID {material_id} 库存不足。当前库存: {current_stock}, 需出库: {quantity_to_outbound}"
    #     )

    # 2. 创建出库记录本身
    db_outbound_record = OutboundRecordModel(**outbound_record_data.model_dump())
    db.add(db_outbound_record)

    # 3. 更新库存余額 (负数表示减少)
    # update_inventory_balance_quantity 内部会检查库存并抛出异常如果不足
    try:
        update_inventory_balance_quantity(db=db, material_id=material_id, quantity_change=-quantity_to_outbound)
        
        # 同样，这里的事务管理需要注意
        db.commit() # 提交出库记录
        db.refresh(db_outbound_record)
    except HTTPException as e:
        db.rollback() # 如果库存更新失败 (例如库存不足的异常)，回滚
        raise e
    except Exception as e_gen:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"创建出库记录时发生未知错误: {str(e_gen)}")

    return db_outbound_record

# 根据ID获取出库记录
def get_outbound_record_by_id(db: Session, record_id: int) -> OutboundRecordModel | None:
    return db.query(OutboundRecordModel).filter(OutboundRecordModel.id == record_id).first()

# 获取出库记录列表 (可分页、可按物资ID、时间范围等过滤)
def get_outbound_records(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    material_id: int | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None
) -> list[OutboundRecordModel]:
    query = db.query(OutboundRecordModel)
    if material_id is not None:
        query = query.filter(OutboundRecordModel.material_id == material_id)
    if start_time:
        query = query.filter(OutboundRecordModel.outbound_time >= start_time)
    if end_time:
        query = query.filter(OutboundRecordModel.outbound_time <= end_time)
    return query.order_by(OutboundRecordModel.outbound_time.desc()).offset(skip).limit(limit).all()