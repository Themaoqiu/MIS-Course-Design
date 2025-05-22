from fastapi import APIRouter
from . import materials
from . import inventory_balances
from . import inbound_records   
from . import outbound_records   
from . import statistics

api_router = APIRouter()

api_router.include_router(materials.router, prefix="/materials", tags=["物资管理 (Materials)"])
api_router.include_router(inventory_balances.router, prefix="/inventory-balances", tags=["库存余額 (Inventory Balances)"])
api_router.include_router(inbound_records.router, prefix="/inbound-records", tags=["入库记录 (Inbound Records)"])
api_router.include_router(outbound_records.router, prefix="/outbound-records", tags=["出库记录 (Outbound Records)"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["统计数据 (Statistics)"]) 