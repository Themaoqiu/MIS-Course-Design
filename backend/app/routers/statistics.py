from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db # 获取数据库会话的依赖项
from app.crud import crud_statistics # 导入上面创建的 CRUD 函数
from app.schemas.statistics import DashboardSummary # 导入响应模型 Schema

router = APIRouter()

@router.get(
    "/dashboard-summary",
    response_model=DashboardSummary, # 指定响应的数据模型
    summary="获取仪表盘概要统计数据",
    description="提供物资种类总数、当前库存总量和库存预警数量等仪表盘核心指标。"
)
def read_dashboard_summary(
    db: Session = Depends(get_db)
    # current_user: schemas.user.User = Depends(get_current_active_user) # 如果需要用户认证
):
    """
    获取仪表盘的概要统计信息：
    - **material_types_count**: 系统中已定义的物资种类的总数。
    - **total_stock_quantity**: 所有物资当前库存数量的总和。
    - **stock_alert_count**: 当前库存量低于最小库存预警线的物资种类数量。
    """
    summary_data = crud_statistics.get_dashboard_summary_data(db)
    return summary_data # FastAPI 会自动将字典转换为 DashboardSummary Schema (如果匹配)