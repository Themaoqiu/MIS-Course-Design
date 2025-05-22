from sqlalchemy.orm import Session # 导入 SQLAlchemy 的会话类型
from app.models.material import Material as MaterialModel # 导入 SQLAlchemy 模型，并重命名以区分 Schema
from app.schemas.material import MaterialCreate, MaterialUpdate # 导入 Pydantic Schema

# 根据 ID 查询单个物资
def get_material_by_id(db: Session, material_id: int) -> MaterialModel | None:
    return db.query(MaterialModel).filter(MaterialModel.id == material_id).first()

# 根据物资编码查询单个物资
def get_material_by_code(db: Session, code: str) -> MaterialModel | None:
    return db.query(MaterialModel).filter(MaterialModel.code == code).first()

# 查询物资列表 (支持分页)
def get_materials(db: Session, skip: int = 0, limit: int = 100) -> list[MaterialModel]:
    return db.query(MaterialModel).offset(skip).limit(limit).all()

# 获取物资总数 (用于分页)
def count_materials(db: Session) -> int:
    return db.query(MaterialModel).count()

# 创建新物资
def create_material(db: Session, material: MaterialCreate) -> MaterialModel:
    # 使用 Pydantic 模型的 model_dump() (V2) 或 dict() (V1) 方法将 Schema 对象转换为字典
    # 然后使用 ** 操作符解包字典，将其作为参数传递给 SQLAlchemy 模型构造函数
    db_material = MaterialModel(**material.model_dump())
    db.add(db_material) # 将新创建的物资对象添加到会话中
    db.commit() # 提交事务，将更改保存到数据库
    db.refresh(db_material) #刷新会话中的 db_material 对象，以获取数据库生成的值 (如 ID, created_at)

    # ---- 重要：创建物资后，初始化其库存余額记录 ----
    from . import crud_inventory_balance # 导入库存余額的 CRUD 操作
    from app.schemas.inventory_balance import InventoryBalanceCreate # 导入库存余額创建 Schema
    initial_balance = InventoryBalanceCreate(material_id=db_material.id, current_quantity=0)
    crud_inventory_balance.create_inventory_balance(db=db, inventory_balance=initial_balance)
    # ---- End ----
    return db_material

# 更新现有物资信息
def update_material(db: Session, material_id: int, material_update: MaterialUpdate) -> MaterialModel | None:
    db_material = get_material_by_id(db, material_id) # 先根据 ID 查找物资
    if not db_material:
        return None # 如果物资不存在，返回 None

    # exclude_unset=True 表示只获取在 material_update 对象中被显式设置了值的字段
    # 这样可以避免将未提供的字段更新为 None
    update_data = material_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_material, key, value) # 动态设置查找到的物资对象的属性值

    db.add(db_material) # 再次添加到会话 (如果对象已存在，SQLAlchemy 会识别为更新)
    db.commit() # 提交事务
    db.refresh(db_material) # 刷新对象
    return db_material

# 删除物资
def delete_material(db: Session, material_id: int) -> MaterialModel | None:
    db_material = get_material_by_id(db, material_id) # 先根据 ID 查找物资
    if not db_material:
        return None # 如果物资不存在，返回 None

    # ---- 重要：删除物资前，应考虑其关联数据 ----
    # 1. 检查库存余額是否为0
    # 2. 检查是否有未完成的入库/出库单
    # 3. 根据业务逻辑决定是逻辑删除 (设置 is_active=False) 还是物理删除
    # 此处为物理删除示例：
    # if db_material.inventory_balance and db_material.inventory_balance.current_quantity != 0:
    #     raise ValueError("Cannot delete material with existing stock.") # 或者返回特定错误码
    # ---- End ----

    db.delete(db_material) # 从会话中删除对象
    db.commit() # 提交事务
    return db_material # 返回被删除的物资对象 (此时它已不在数据库中)