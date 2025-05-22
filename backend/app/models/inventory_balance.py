from sqlalchemy import Column, Integer, ForeignKey, DateTime, func 
from app.db.database import Base
from sqlalchemy.orm import relationship 

class InventoryBalance(Base):
    # 库存余额
    __tablename__ = "inventory_balance"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) # 库存余額记录 ID，主键，自增
    material_id = Column(Integer, ForeignKey("materials.id"), unique=True, nullable=False, index=True) # 关联的物资 ID，外键，唯一，不能为空，建立索引
    current_quantity = Column(Integer, nullable=False, default=0) # 当前库存数量，不能为空，默认为 0
    min_stock_level = Column(Integer, nullable=True, default=0) # 最低库存阈值 (预警用)，可为空，默认为 0
    max_stock_level = Column(Integer, nullable=True, default=0) # 最高库存阈值 (预警用)，可为空，默认为 0
    last_updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()) # 最后更新时间

    # 定义与 Material 模型的关系 (一对一)
    # `back_populates` 用于双向关系，在 Material 模型中也需要定义对应的 relationship
    material = relationship("Material", back_populates="inventory_balance")