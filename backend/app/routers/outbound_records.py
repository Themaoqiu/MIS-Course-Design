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
    response_model=schemas.outbound_record.OutboundRecord,
    status_code=status.HTTP_201_CREATED,
    summary="创建出库记录",
    description="创建一个新的物资出库记录，系统会自动检查库存是否充足并更新相应物资的库存余額。"
)
def create_new_outbound_record(
    outbound_data: schemas.outbound_record.OutboundRecordCreate,
    db: Session = Depends(get_db)
    # current_user: schemas.user.User = Depends(get_current_user) # 权限控制
):
    # 检查物资是否存在
    material_for_outbound = crud.crud_material.get_material_by_id(db, material_id=outbound_data.material_id) # 假设你有 crud_material
    if not material_for_outbound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"无法创建出库记录：物资ID {outbound_data.material_id} 不存在。"
        )
        
    try:
        return crud.crud_outbound_record.create_outbound_record(db=db, outbound_record_data=outbound_data)
    except HTTPException as e: # 例如库存不足的异常
        raise e
    except Exception as e_global:
        # Log the error e_global
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"创建出库记录时发生内部错误: {str(e_global)}")


@router.get(
    "/",
    response_model=List[schemas.outbound_record.OutboundRecord],
    summary="获取出库记录列表 (UC7)",
    description="获取出库记录列表，支持分页和按物资ID、时间范围过滤。"
)
def read_all_outbound_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    material_id: Optional[int] = Query(None, description="按物资ID过滤"),
    start_time: Optional[datetime] = Query(None, description="按出库开始时间过滤 (ISO格式 YYYY-MM-DDTHH:MM:SS)"),
    end_time: Optional[datetime] = Query(None, description="按出库结束时间过滤 (ISO格式 YYYY-MM-DDTHH:MM:SS)"),
    db: Session = Depends(get_db)
):
    records = crud.crud_outbound_record.get_outbound_records(
        db, skip=skip, limit=limit, material_id=material_id, start_time=start_time, end_time=end_time
    )
    return records

@router.get(
    "/{record_id}",
    response_model=schemas.outbound_record.OutboundRecord,
    summary="获取单个出库记录详情 (UC7)",
    description="根据记录ID获取出库记录的详细信息。"
)
def read_single_outbound_record(record_id: int, db: Session = Depends(get_db)):
    record = crud.crud_outbound_record.get_outbound_record_by_id(db, record_id=record_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="出库记录未找到")
    return record