from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Text
from app.db.database import Base
from sqlalchemy.orm import relationship

class OutboundRecord(Base):
    # 出库记录表
    __tablename__ = "outbound_records" # 表名修正

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) # ID，主键，索引，自增
    outbound_order_number = Column(String(100), unique=True, index=True, nullable=True, comment="出库单号") # 新增：出库单号，唯一，索引
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False, index=True) # 关联的物资 ID，外键，不能为空，建立索引 (移除了 unique=True)
    quantity = Column(Integer, nullable=False, comment="出库数量") # 新增：出库数量，不能为空
    recipient = Column(String(255), nullable=True, comment="领用人或客户") # 新增：领用人/客户
    outbound_time = Column(DateTime(timezone=True), default=func.now(), nullable=False, comment="出库时间") # 出库时间，默认为当前时间，不能为空 (comment 修正, nullable 改为 False)
    remarks = Column(Text, nullable=True, comment="备注") # 新增：备注

    # 与 Material 模型的关系 (多对一)
    material = relationship("Material", viewonly=True) #