from sqlalchemy import Column, Integer, String, Text, DateTime, func, Boolean 
from app.db.database import Base
from sqlalchemy.orm import relationship

class Material(Base):
    __tablename__ = "materials" # 定义数据库中的表名

    # 定义表的列 (字段)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) # 物资 ID，主键，自增，建立索引
    code = Column(String(100), unique=True, index=True, nullable=False) # 物资编码，唯一，建立索引，不能为空
    name = Column(String(255), nullable=False, index=True) # 物资名称，不能为空，建立索引
    model = Column(String(255), nullable=True) # 型号，可为空
    unit = Column(String(50), nullable=True) # 单位 (如: 个, 箱, 千克)，可为空
    supplier = Column(String(255), nullable=True) # 供应商，可为空
    remarks = Column(Text, nullable=True) # 备注，可为空
    is_active = Column(Boolean, default=True) # 标记物资是否启用，默认为 True

    # 时间戳
    # server_default=func.now() 表示创建记录时由数据库服务器生成当前时间
    # default=func.now() 表示创建记录时由应用服务器生成当前时间 (如果数据库不支持 server_default)
    # onupdate=func.now() 表示记录更新时自动更新时间
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # 创建时间
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()) # 更新时间

    inventory_balance = relationship(
        "InventoryBalance",
        back_populates="material",
        uselist=False,
        cascade="all, delete-orphan"  # <--- 添加这个配置
    )