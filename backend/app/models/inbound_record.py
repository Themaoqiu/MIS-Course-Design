from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Text
from app.db.database import Base
from sqlalchemy.orm import relationship

class InboundRecord(Base):
    # 入库记录表
    __tablename__ = "inbound_records" # 表名修正为复数形式

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) # ID，主键，索引，自增
    inbound_order_number = Column(String(100), unique=True, index=True, nullable=True, comment="入库单号") # 新增：入库单号，唯一，索引
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False, index=True) # 关联的物资 ID，外键，不能为空，建立索引 
    quantity = Column(Integer, nullable=False, comment="入库数量") # 新增：入库数量，不能为空
    inbound_time = Column(DateTime(timezone=True), default=func.now(), nullable=False, comment="入库时间") # 入库时间，默认为当前时间，不能为空
    remarks = Column(Text, nullable=True, comment="备注") # 新增：备注

    # 与 Material 模型的关系 (多对一)
    # viewonly=True 表示这个关系仅用于查询，SQLAlchemy 不会尝试通过这个关系来管理另一端
    material = relationship("Material", viewonly=True) 