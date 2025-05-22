# app/crud/crud_statistics.py
from sqlalchemy.orm import Session
from sqlalchemy import func # 用于聚合函数如 count, sum
from app.models.material import Material as MaterialModel # 导入物资模型
from app.models.inventory_balance import InventoryBalance as InventoryBalanceModel # 导入库存余額模型

def get_dashboard_summary_data(db: Session) -> dict:
    # 1. 物资种类总数
    material_types_count = db.query(func.count(MaterialModel.id)).scalar() or 0

    # 2. 当前库存总量
    total_stock_quantity_query = db.query(func.sum(InventoryBalanceModel.current_quantity)).scalar()
    total_stock_quantity = total_stock_quantity_query if total_stock_quantity_query is not None else 0


    # 3. 库存预警数量
    # (当 current_quantity < min_stock_level 且 min_stock_level > 0 时视为预警)
    stock_alert_count = db.query(func.count(InventoryBalanceModel.id)).filter(
        InventoryBalanceModel.current_quantity < InventoryBalanceModel.min_stock_level,
        InventoryBalanceModel.min_stock_level > 0 # 确保最低库存设置了才有意义
    ).scalar() or 0

    return {
        "material_types_count": material_types_count,
        "total_stock_quantity": total_stock_quantity,
        "stock_alert_count": stock_alert_count,
    }