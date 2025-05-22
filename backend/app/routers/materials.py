from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional 
from sqlalchemy import or_
from app import schemas 
from app import crud
from app.db.database import get_db 

router = APIRouter() # 创建一个新的 API 路由器实例

# 定义 API 端点 (Endpoint)

@router.post(
    "/",
    response_model=schemas.material.Material, # 定义成功响应的数据模型 (返回给客户端的格式)
    status_code=status.HTTP_201_CREATED, # 定义成功创建资源时的 HTTP 状态码
    summary="创建新物资",
    description="根据提供的信息创建一个新的物资条目，并为其初始化库存余額。"
)
def create_new_material(
    material_in: schemas.material.MaterialCreate, # 请求体数据，将由 Pydantic 自动校验
    db: Session = Depends(get_db) # 依赖注入：获取数据库会话
):
    db_material_by_code = crud.crud_material.get_material_by_code(db, code=material_in.code)
    if db_material_by_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"物资编码 '{material_in.code}' 已存在.")
    created_material = crud.crud_material.create_material(db=db, material=material_in)

    return created_material


@router.get(
    "/",
    response_model=schemas.material.MaterialPage,
    summary="获取物资列表",
    description="获取所有物资的列表，支持分页和基于名称或编码的简单过滤。"
)
@router.get(
    "/",
    response_model=schemas.material.MaterialPage,
    summary="获取物资列表",
    description="获取所有物资的列表，支持分页和基于名称、编码或激活状态的过滤。"
)
def read_all_materials(
    skip: int = Query(0, ge=0, description="跳过的记录数 (用于分页)"),
    # 你可以根据需要调整 limit 的最大值，例如 le=1000，如果前端确实需要那么多
    limit: int = Query(10, ge=1, le=200, description="每页返回的记录数 (例如最大200)"),
    code: Optional[str] = Query(None, description="按物资编码模糊过滤"),
    name: Optional[str] = Query(None, description="按物资名称模糊过滤"),
    is_active: Optional[bool] = Query(None, description="按激活状态过滤 (true 或 false)"), # <--- 添加 is_active 参数
    db: Session = Depends(get_db)
):
    materials_query = db.query(crud.crud_material.MaterialModel) #

    filter_conditions = []

    # 原有的名称和编码过滤
    if name and code:
        filter_conditions.append(
            or_(
                crud.crud_material.MaterialModel.name.ilike(f"%{name}%"),
                crud.crud_material.MaterialModel.code.ilike(f"%{code}%")
            )
        )
    elif name:
        filter_conditions.append(crud.crud_material.MaterialModel.name.ilike(f"%{name}%"))
    elif code:
        filter_conditions.append(crud.crud_material.MaterialModel.code.ilike(f"%{code}%"))

    # 新增的 is_active 过滤
    if is_active is not None: # 只有当 is_active 参数被提供时才应用过滤
        filter_conditions.append(crud.crud_material.MaterialModel.is_active == is_active)

    if filter_conditions:
        materials_query = materials_query.filter(*filter_conditions)

    total = materials_query.count()
    items = materials_query.order_by(crud.crud_material.MaterialModel.id.desc()).offset(skip).limit(limit).all() # 添加排序示例

    return schemas.material.MaterialPage(
        items=items,
        total=total,
        page=(skip // limit) + 1,
        size=limit,
        pages=(total + limit - 1) // limit if total > 0 else 0
    )

@router.get(
    "/{material_id}",
    response_model=schemas.material.Material,
    summary="获取单个物资详情",
    description="根据物资 ID 获取其详细信息。"
)
def read_single_material(material_id: int, db: Session = Depends(get_db)):
    db_material = crud.crud_material.get_material_by_id(db, material_id=material_id)
    if db_material is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="物资未找到")
    return db_material

@router.put(
    "/{material_id}",
    response_model=schemas.material.Material,
    summary="更新物资信息",
    description="根据物资 ID 更新其部分或全部信息。"
)
def update_existing_material(
    material_id: int,
    material_in: schemas.material.MaterialUpdate, # 请求体数据
    db: Session = Depends(get_db)
):
    db_material = crud.crud_material.get_material_by_id(db, material_id=material_id)
    if db_material is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="物资未找到")

    # 如果请求中包含物资编码，且该编码与当前物资编码不同，则检查新编码是否已存在
    if material_in.code and material_in.code != db_material.code:
        existing_material_with_new_code = crud.crud_material.get_material_by_code(db, code=material_in.code)
        if existing_material_with_new_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"物资编码 '{material_in.code}' 已被其他物资使用."
            )

    updated_material = crud.crud_material.update_material(db, material_id=material_id, material_update=material_in)
    return updated_material # update_material 内部已处理了不存在的情况，但为清晰起见再次检查

@router.delete(
    "/{material_id}",
    response_model=schemas.material.Material,
    summary="删除物资",
    description="根据物资 ID 删除一个物资。注意：删除前应检查库存是否为零。"
)
def delete_existing_material(
    material_id: int,
    db: Session = Depends(get_db)
):
    # 检查物资是否存在
    db_material_to_delete = crud.crud_material.get_material_by_id(db, material_id=material_id)
    if db_material_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="物资未找到")

    # ---- 业务逻辑：删除前的检查 ----
    # 检查关联的库存余額是否为零
    balance_record = crud.crud_inventory_balance.get_inventory_balance_by_material_id(db, material_id=material_id)
    if balance_record and balance_record.current_quantity > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无法删除物资 '{db_material_to_delete.name}'，因为其当前库存不为零 ({balance_record.current_quantity} {db_material_to_delete.unit})."
        )

    # 执行删除 (crud_material.delete_material 内部应处理关联库存余額记录的删除，或通过数据库外键级联删除)
    deleted_material = crud.crud_material.delete_material(db, material_id=material_id)
    if deleted_material is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="物资删除过程中未找到")

    if balance_record:
       crud.crud_inventory_balance.delete_inventory_balance(db, balance_id=balance_record.id)
    return deleted_material