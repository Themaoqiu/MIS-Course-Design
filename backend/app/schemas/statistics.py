# app/schemas/statistics.py
from pydantic import BaseModel

class DashboardSummary(BaseModel):
    material_types_count: int
    total_stock_quantity: int
    stock_alert_count: int

    class Config:
        from_attributes = True # Pydantic V2 (或 orm_mode = True for V1)