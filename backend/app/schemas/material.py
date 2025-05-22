from pydantic import BaseModel, Field # 从 Pydantic 导入 BaseModel 和 Field 用于数据校验
from typing import Optional # 用于定义可选字段
from datetime import datetime

# 物资基础 Schema，包含所有模型共有的字段
class MaterialBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=100, description="物资编码，必填") 
    name: str = Field(..., min_length=1, max_length=255, description="物资名称，必填")
    model: Optional[str] = Field(None, max_length=255, description="型号")
    unit: Optional[str] = Field(None, max_length=50, description="单位")
    supplier: Optional[str] = Field(None, max_length=255, description="供应商")
    remarks: Optional[str] = Field(None, description="备注")
    is_active: Optional[bool] = Field(True, description="是否启用")


class MaterialCreate(MaterialBase):
    pass 

# 更新物资时请求体中允许包含的字段
# 所有字段都设为可选，因为更新时可能只更新部分信息
class MaterialUpdate(BaseModel):
    code: Optional[str] = Field(None, min_length=1, max_length=100, description="物资编码")
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="物资名称")
    model: Optional[str] = Field(None, max_length=255, description="型号")
    unit: Optional[str] = Field(None, max_length=50, description="单位")
    supplier: Optional[str] = Field(None, max_length=255, description="供应商")
    remarks: Optional[str] = Field(None, description="备注")
    is_active: Optional[bool] = Field(None, description="是否启用")


# 从数据库读取物资信息并返回给客户端时，响应体中包含的字段
class MaterialResponse(MaterialBase):
    id: int 
    created_at: datetime 
    updated_at: datetime 

    # 这个配置允许 Pydantic 模型直接从 SQLAlchemy 模型实例 (ORM对象) 创建和填充数据
    class Config:
        from_attributes = True

# 返回给客户端的最终物资信息 Schema
class Material(MaterialResponse):
    pass

class MaterialPage(BaseModel):
    items: list[Material]
    total: int
    page: int
    size: int
    pages: int