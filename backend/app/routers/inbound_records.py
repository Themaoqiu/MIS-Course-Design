from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app import schemas
from app import crud
from app.db.database import get_db

router = APIRouter()

@router.post(
    "/",
    response_model=schemas.inbound_record.InboundRecord,
    status_code=status.HTTP_201_CREATED,
    summary="创建入库记录 (UC2)",
    description="创建一个新的物资入库记录，并自动更新相应物资的库存余額。"
)
def create_new_inbound_record(
    inbound_data: schemas.inbound_record.InboundRecordCreate,
    db: Session = Depends(get_db)
    # current_user: schemas.user.User = Depends(get_current_user) # 权限控制
):
    # 检查物资是否存在 (可选，如果外键约束处理不了所有情况，或者想提供更友好的错误信息)
    material_for_inbound = crud.crud_material.get_material_by_id(db, material_id=inbound_data.material_id) # 假设你有 crud_material
    if not material_for_inbound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"无法创建入库记录：物资ID {inbound_data.material_id} 不存在。"
        )
    
    try:
        return crud.crud_inbound_record.create_inbound_record(db=db, inbound_record_data=inbound_data)
    except HTTPException as e: # 捕获 CRUD 层可能抛出的特定业务异常
        raise e
    except Exception as e_global: # 捕获其他意外错误
        # Log the error e_global for debugging
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"创建入库记录时发生内部错误: {str(e_global)}")


@router.get(
    "/",
    response_model=List[schemas.inbound_record.InboundRecord],
    summary="获取入库记录列表",
    description="获取入库记录列表，支持分页和按物资ID、时间范围过滤。"
)
def read_all_inbound_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    material_id: Optional[int] = Query(None, description="按物资ID过滤"),
    start_time: Optional[datetime] = Query(None, description="按入库开始时间过滤 (ISO格式 YYYY-MM-DDTHH:MM:SS)"),
    end_time: Optional[datetime] = Query(None, description="按入库结束时间过滤 (ISO格式 YYYY-MM-DDTHH:MM:SS)"),
    db: Session = Depends(get_db)
):
    records = crud.crud_inbound_record.get_inbound_records(
        db, skip=skip, limit=limit, material_id=material_id, start_time=start_time, end_time=end_time
    )
    return records

@router.get(
    "/{record_id}",
    response_model=schemas.inbound_record.InboundRecord,
    summary="获取单个入库记录详情",
    description="根据记录ID获取入库记录的详细信息。"
)
def read_single_inbound_record(record_id: int, db: Session = Depends(get_db)):
    record = crud.crud_inbound_record.get_inbound_record_by_id(db, record_id=record_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="入库记录未找到")
    return record