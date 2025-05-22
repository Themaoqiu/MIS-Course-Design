from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.material import Material

class InboundRecordBase(BaseModel):
    material_id: int = Field(..., description="关联的物资 ID，必填")
    quantity: int = Field(..., gt=0, description="入库数量, 必须大于0") # gt=0 表示大于0
    inbound_order_number: Optional[str] = Field(None, max_length=100, description="入库单号")
    remarks: Optional[str] = Field(None, description="备注")

class InboundRecordCreate(InboundRecordBase):
    pass

class InboundRecord(InboundRecordBase):
    id: int
    inbound_time: datetime
    material: Optional[Material] = None

    class Config:
        orm_mode = True

