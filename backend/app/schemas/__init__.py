from .material import Material  # 显式导入
from .inbound_record import InboundRecord
from .outbound_record import OutboundRecord
from .inventory_balance import InventoryBalance

__all__ = ["Material", "InboundRecord", "OutboundRecord"]  # 可选，但推荐