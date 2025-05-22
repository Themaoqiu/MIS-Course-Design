from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.material import Material as MaterialSchema

# 出库记录基础 Schema
class OutboundRecordBase(BaseModel):
    material_id: int = Field(..., description="物资ID")
    quantity: int = Field(..., gt=0, description="出库数量, 必须大于0")
    outbound_order_number: Optional[str] = Field(None, max_length=100, description="出库单号")
    recipient: Optional[str] = Field(None, max_length=255, description="领用人或客户")
    remarks: Optional[str] = Field(None, description="备注")

# 创建出库记录时请求体中需要包含的字段
class OutboundRecordCreate(OutboundRecordBase):
    pass

# 从数据库读取并返回给客户端的出库记录信息
class OutboundRecord(OutboundRecordBase):
    id: int
    outbound_time: datetime
    material: Optional[MaterialSchema] = None # 关联的物资信息

    class Config:
        from_attributes = True