from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.material import Material

class InventoryBalanceBase(BaseModel):
    material_id: int = Field(..., description="关联的物资 ID，必填")
    current_quantity: int = Field(default=0, description="当前库存数量，默认为 0")
    min_stock_level: Optional[int] = Field(default=0, description="最低库存阈值，可选，默认为 0")
    max_stock_level: Optional[int] = Field(default=0, description="最高库存阈值，可选，默认为 0")

class InventoryBalanceCreate(InventoryBalanceBase):
    pass

class InventoryBalanceUpdate(BaseModel):
    current_quantity: Optional[int] = Field(None, description="更新的库存数量，可选")
    min_stock_level: Optional[int] = Field(None, description="更新的最低库存阈值，可选")
    max_stock_level: Optional[int] = Field(None, description="更新的最高库存阈值，可选")

class InventoryBalance(InventoryBalanceBase):
    id: int
    last_updated_at: datetime
    material: Optional[Material] = None

    class Config:
        orm_mode = True 

